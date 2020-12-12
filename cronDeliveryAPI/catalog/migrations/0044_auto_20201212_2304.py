# Generated by Django 3.0.8 on 2020-12-12 23:04

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0043_auto_20201202_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='cart',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='items', to='catalog.Cart', verbose_name='Корзина'),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='worksFrom',
            field=models.TimeField(default=datetime.datetime(2020, 12, 12, 23, 4, 2, 864577)),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='worksTo',
            field=models.TimeField(default=datetime.datetime(2020, 12, 12, 23, 4, 2, 864599)),
        ),
    ]
