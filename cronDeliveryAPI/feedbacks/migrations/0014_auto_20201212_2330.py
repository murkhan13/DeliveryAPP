# Generated by Django 3.0.8 on 2020-12-12 23:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedbacks', '0013_auto_20201212_2304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderfeedback',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 12, 23, 30, 36, 563158), verbose_name='Заказ создан'),
        ),
        migrations.AlterField(
            model_name='restaurantfeedback',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 12, 23, 30, 36, 562663), verbose_name='Отзыв добавлен создан'),
        ),
    ]
