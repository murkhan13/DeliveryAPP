# Generated by Django 3.0.8 on 2020-08-17 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0025_auto_20200807_1953'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='deliveryTime',
            field=models.IntegerField(default=60, verbose_name='Среднее время доставки(мин)'),
        ),
    ]
