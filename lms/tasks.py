from celery import shared_task
from django.conf.global_settings import EMAIL_HOST_USER
from django.utils import timezone

from lms.models import Subscription
import smtplib
from django.core.mail import send_mail


@shared_task
def mailing_about_updates(well_id):
    """Функция отправления сообщений об обновлении курса клиентам"""
    subscriptions = Subscription.objects.filter(well_id=well_id, is_active=True)
    for subscription in subscriptions:
        if subscription.well.last_update < timezone.now() + timezone.timedelta(hours=4):
            try:
                send_mail(
                    subject='Обновление подписки на курс',
                    message=f'Курс {subscription.well.title} был обновлен.',
                    from_email=EMAIL_HOST_USER,
                    recipient_list=[subscription.user.email],
                    fail_silently=False,
                )
            except smtplib.SMTPException:
                raise smtplib.SMTPException
