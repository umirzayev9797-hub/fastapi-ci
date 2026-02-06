import json
import os
from flask import Flask, request, jsonify
from celery.result import GroupResult
from celery import group
from celery_app import app as celery_app  # Импортируем наше Celery-приложение
from tasks import process_single_image
import config

app = Flask(__name__)


# Помощники для работы с "базой данных" подписчиков
def get_subs():
    if not os.path.exists(config.SUBSCRIBERS_FILE): return set()
    with open(config.SUBSCRIBERS_FILE, 'r') as f: return set(json.load(f))


def save_subs(subs):
    with open(config.SUBSCRIBERS_FILE, 'w') as f: json.dump(list(subs), f)


@app.route('/blur', methods=['POST'])
def blur():
    data = request.json
    email = data.get('email')
    filenames = data.get('images', [])
    order_id = "ORD-" + os.urandom(3).hex()

    # Создаем группу задач
    job_group = group(process_single_image.s(order_id, email, f) for f in filenames)
    result = job_group.apply_async()

    # Сохраняем группу в бэкенд (Redis)
    result.save()
    return jsonify({"group_id": result.id}), 202


@app.route('/status/<group_id>', methods=['GET'])
def get_status(group_id):
    # ВАЖНО: передаем app=celery_app, чтобы не было ошибки DisabledBackend
    res = GroupResult.restore(group_id, app=celery_app)

    if not res:
        return jsonify({"error": "Group result not found. Check if Redis is running and result_backend is set."}), 404

    return jsonify({
        "total": len(res.results),
        "completed": res.completed_count(),
        "status": "Ready" if res.ready() else "Processing"
    })


@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.json.get('email')
    subs = get_subs()
    subs.add(email)
    save_subs(subs)
    return jsonify({"message": f"{email} subscribed"}), 200


@app.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    email = request.json.get('email')
    subs = get_subs()
    subs.discard(email)
    save_subs(subs)
    return jsonify({"message": f"{email} unsubscribed"}), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)