# Generated by Django 3.0.8 on 2020-08-10 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_order_restaurant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='restaurant',
            field=models.CharField(blank=True, default=None, max_length=200, null=True, verbose_name='Ресторан'),
        ),
    ]
