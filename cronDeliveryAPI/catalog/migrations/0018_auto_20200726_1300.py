# Generated by Django 3.0.8 on 2020-07-26 10:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0010_remove_order_order_items'),
        ('catalog', '0017_cartitem_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='likedUsers',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='additives',
            field=models.ManyToManyField(to='catalog.DishAdditive', verbose_name='Добавки'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='cart',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='catalog.Cart', verbose_name='Корзина'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='category',
            field=models.ManyToManyField(to='catalog.Category', verbose_name='Категории'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='extra',
            field=models.ManyToManyField(to='catalog.DishExtra', verbose_name='Дополнительно'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_items', to='orders.Order', verbose_name='Заказ'),
        ),
    ]