"""
В этом файле будут секретные данные

Для создания почтового сервиса воспользуйтесь следующими инструкциями

- Yandex: https://yandex.ru/support/mail/mail-clients/others.html
- Google: https://support.google.com/mail/answer/7126229?visit_id=638290915972666565-928115075
"""

# https://yandex.ru/support/mail/mail-clients/others.html

import os

SMTP_USER = "uhope474@ya.ru"
SMTP_HOST = "smtp.yandex.com"
SMTP_PASSWORD = "xrsyiteokzpolzvy"
SMTP_PORT = 587

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

# Путь для хранения подписчиков
SUBSCRIBERS_FILE = 'subscribers.json'
# Папка для обработки изображений
UPLOAD_FOLDER = 'images'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
