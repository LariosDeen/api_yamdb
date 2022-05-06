# Generated by Django 2.2.16 on 2022-05-06 13:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(limit_value=1, message='Минимальная оценка 1'), django.core.validators.MaxValueValidator(limit_value=10, message='Максимальная оценка 10')], verbose_name='Оценка произведения'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('user', 'User'), ('admin', 'Administrator'), ('moderator', 'Moderator')], default='user', max_length=50, verbose_name='Роль'),
        ),
    ]