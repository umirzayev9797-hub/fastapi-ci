from celery import Celery
from celery.schedules import crontab
import config

app = Celery(
    'image_service',
    broker=config.CELERY_BROKER_URL,
    backend=config.CELERY_RESULT_BACKEND,
    include=['tasks']
)

# Настройка Celery Beat для еженедельной рассылки
app.conf.beat_schedule = {
    'weekly-newsletter': {
        'task': 'tasks.send_weekly_newsletter',
        'schedule': crontab(day_of_week=1, hour=9, minute=0), # Понедельник, 9:00
    },
}

app.conf.timezone = 'UTC'