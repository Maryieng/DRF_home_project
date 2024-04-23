from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Well(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    preview = models.ImageField(upload_to='preview/', verbose_name='Изображение', **NULLABLE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    preview = models.ImageField(upload_to='preview/', verbose_name='Изображение', **NULLABLE)
    will = models.ForeignKey('Well', on_delete=models.CASCADE, verbose_name='Курс', **NULLABLE)
    video_link = models.CharField(max_length=300, verbose_name='Ссылка на видео', **NULLABLE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
