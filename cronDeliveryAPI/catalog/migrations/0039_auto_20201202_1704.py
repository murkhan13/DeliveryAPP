# Generated by Django 3.0.8 on 2020-12-02 17:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0038_auto_20201202_1417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='worksFrom',
            field=models.TimeField(default=datetime.datetime(2020, 12, 2, 17, 4, 21, 295044)),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='worksTo',
            field=models.TimeField(default=datetime.datetime(2020, 12, 2, 17, 4, 21, 295098)),
        ),
    ]
