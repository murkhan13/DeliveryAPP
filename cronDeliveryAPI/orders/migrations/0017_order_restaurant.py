# Generated by Django 3.0.8 on 2020-08-17 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0016_remove_order_restaurant'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='restaurant',
            field=models.CharField(default='нет', max_length=200, verbose_name='Ресторан'),
        ),
    ]
