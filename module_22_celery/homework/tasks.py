import json
import os
from celery_app import app
from image import blur_image
from mail import send_email
import config


@app.task(bind=True)
def process_single_image(self, order_id, email, filename):
    """Задача на обработку одного фото и отправку его на почту"""
    output_filename = f"blur_{filename}"
    # Пути к файлам (предполагаем, что они в папке images)
    src_path = os.path.join(config.UPLOAD_FOLDER, filename)
    dst_path = os.path.join(config.UPLOAD_FOLDER, output_filename)

    blur_image(src_path, dst_path)
    send_email(order_id, email, dst_path)
    return True


@app.task
def send_weekly_newsletter():
    """Периодическая задача: рассылка всем подписчикам"""
    if not os.path.exists(config.SUBSCRIBERS_FILE):
        return "No subscribers"

    with open(config.SUBSCRIBERS_FILE, 'r') as f:
        subscribers = json.load(f)

    for email in subscribers:
        # В реальном проекте здесь был бы шаблон письма
        print(f"Sending newsletter to {email}")
        # send_email("Newsletter", email, "news.pdf")

    return f"Newsletter sent to {len(subscribers)} users"