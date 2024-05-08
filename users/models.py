from django.utils import timezone
from typing import List

from django.contrib.auth.models import AbstractUser
from django.db import models

from lms.models import Well, Lesson

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):

    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')
    phone = models.CharField(max_length=35, verbose_name='Телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', **NULLABLE)
    city = models.CharField(max_length=50, verbose_name='Город', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: List[str] = []

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, **NULLABLE)
    well = models.ForeignKey(Well, on_delete=models.DO_NOTHING, **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.DO_NOTHING, **NULLABLE)
    method_pay = models.CharField(max_length=15, choices=(('cash', 'наличными'), ('card', 'картой')))
    date_payment = models.DateField(default=timezone.now, **NULLABLE)
    money = models.IntegerField()
    link = models.URLField(max_length=400, verbose_name='Ссылка на оплату', **NULLABLE)

    def __str__(self):
        return f"{self.method_pay}"

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
