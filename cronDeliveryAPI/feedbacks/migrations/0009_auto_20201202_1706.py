# Generated by Django 3.0.8 on 2020-12-02 17:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedbacks', '0008_auto_20201202_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderfeedback',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 2, 17, 6, 10, 523962), verbose_name='Заказ создан'),
        ),
        migrations.AlterField(
            model_name='restaurantfeedback',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 2, 17, 6, 10, 523303), verbose_name='Отзыв добавлен создан'),
        ),
    ]