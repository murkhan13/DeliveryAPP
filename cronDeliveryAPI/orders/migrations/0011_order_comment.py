# Generated by Django 3.0.8 on 2020-07-30 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_remove_order_order_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='comment',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Комментарий'),
        ),
    ]
