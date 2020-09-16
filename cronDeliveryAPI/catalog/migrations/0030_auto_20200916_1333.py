# Generated by Django 3.0.8 on 2020-09-16 10:33

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0029_auto_20200913_1752'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='restaurant',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Ресторан'),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='worksFrom',
            field=models.TimeField(default=datetime.datetime(2020, 9, 16, 10, 33, 13, 908271, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='worksTo',
            field=models.TimeField(default=datetime.datetime(2020, 9, 16, 10, 33, 13, 908271, tzinfo=utc)),
        ),
    ]