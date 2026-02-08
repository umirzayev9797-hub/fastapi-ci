from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)

# Инициализация метрик
metrics = PrometheusMetrics(app)

# Кастомный counter:
# считает количество запросов и коды ответа
request_counter = metrics.counter(
    "custom_requests_total",
    "Total requests with status code",
    labels={"endpoint": lambda: "/", "status": lambda r: r.status_code}
)

@app.route("/")
@request_counter
def home():
    return jsonify(message="Hello World"), 200


@app.route("/error")
@request_counter
def error():
    return jsonify(error="Something went wrong"), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
