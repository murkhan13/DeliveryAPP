# Generated by Django 3.0.8 on 2020-12-12 23:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedbacks', '0012_auto_20201202_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderfeedback',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 12, 23, 4, 2, 872792), verbose_name='Заказ создан'),
        ),
        migrations.AlterField(
            model_name='restaurantfeedback',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 12, 23, 4, 2, 872285), verbose_name='Отзыв добавлен создан'),
        ),
    ]
