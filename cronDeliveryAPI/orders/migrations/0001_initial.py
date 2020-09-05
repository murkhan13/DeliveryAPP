# Generated by Django 3.0.8 on 2020-07-07 10:41

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message="Номер телефона должен быть в формате: '+999999999'.Разрешено до 14 цифр.", regex='^\\+?1?\\d{9,14}$')], verbose_name='Номер телефона')),
                ('total', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='Итоговая сумма')),
                ('deliverTo', models.CharField(max_length=255, verbose_name='Доставить к')),
                ('address', models.CharField(max_length=255, verbose_name='Адрес')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(blank=True, null=True, verbose_name='Количество')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='orders.Order')),
                ('order_dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.CartItem')),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(max_length=255, verbose_name='Улица')),
                ('building', models.CharField(max_length=255, verbose_name='Дом')),
                ('porch', models.CharField(blank=True, max_length=255, null=True, verbose_name='Подъезд')),
                ('floor', models.CharField(blank=True, max_length=255, null=True, verbose_name='Этаж')),
                ('apartment', models.CharField(blank=True, max_length=255, null=True, verbose_name='Квартира')),
                ('comment', models.CharField(blank=True, max_length=255, null=True, verbose_name='Комментарий')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='adresses', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Адрес',
            },
        ),
    ]