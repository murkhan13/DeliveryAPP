# Generated by Django 3.0.8 on 2020-07-25 09:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0016_auto_20200724_1432'),
        ('orders', '0007_auto_20200725_0127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Заказ создан'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order_dish',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.CartItem'),
        ),
    ]
