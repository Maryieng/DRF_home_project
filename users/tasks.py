from celery import shared_task
from calendar import monthrange
from datetime import datetime, timedelta
from users.models import User
import pytz
from django.conf import settings


@shared_task
def check_user_activity():
    """ Блокировка пользователя если он не заходил более месяца на платформу """
    zone = pytz.timezone(settings.TIME_ZONE)
    now = datetime.now(zone)
    month = now.month
    year = now.year
    days_count = monthrange(year, month)
    expiration_date = now - timedelta(days=days_count[1])
    user_list = User.objects.filter(last_login__lte=expiration_date, is_active=True)
    user_list.update(is_active=False)
