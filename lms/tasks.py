from celery import shared_task
from django.conf.global_settings import EMAIL_HOST_USER

from lms.models import Well
import smtplib
from django.core.mail import send_mail


def send_mailing(address, subject, body):
    """Функция отправки письма"""
    try:
        response = send_mail(
            subject=subject,
            message=body,
            from_email=EMAIL_HOST_USER,
            recipient_list=address,
            fail_silently=False,
        )
        return response
    except smtplib.SMTPException:
        raise smtplib.SMTPException


@shared_task
def mailing_about_updates(well_id):
    """Функция отправления сообщений об обновлении курса клиентам"""
    well = Well.objects.get(pk=well_id)
    subscription_list = well.subscription.all()
    user_list = [subscription.user for subscription in subscription_list]
    subject = 'Обновление курса'
    body = f'Вышло обновление по курсу {well}'
    send_mailing(user_list, subject, body)
