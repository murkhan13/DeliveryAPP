# Generated by Django 3.0.8 on 2020-11-28 21:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0034_auto_20201103_0144'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchingCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите категорию блюда(например, супы, салаты, пицца и т.д.', max_length=200, verbose_name='Название категории')),
                ('image', models.ImageField(default='not_found.jpg', upload_to='category_imgs', verbose_name='Картинка блюда')),
            ],
            options={
                'verbose_name': 'Категория для для поиска',
            },
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='worksFrom',
            field=models.TimeField(default=datetime.datetime(2020, 11, 28, 21, 35, 55, 588048)),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='worksTo',
            field=models.TimeField(default=datetime.datetime(2020, 11, 28, 21, 35, 55, 588064)),
        ),
    ]
