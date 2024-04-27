# Generated by Django 5.0.4 on 2024-04-27 08:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0002_alter_lesson_will'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='will',
        ),
        migrations.AddField(
            model_name='lesson',
            name='well',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lms.well', verbose_name='Курс'),
        ),
    ]
