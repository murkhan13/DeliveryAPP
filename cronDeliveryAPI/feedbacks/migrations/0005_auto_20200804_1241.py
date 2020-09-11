# Generated by Django 3.0.8 on 2020-08-04 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedbacks', '0004_auto_20200801_2013'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderfeedbackimage',
            name='image',
            field=models.ImageField(default='not_found.jpg', upload_to='feedbacks', verbose_name='Картинка ресторана'),
        ),
        migrations.AddField(
            model_name='restaurantfeedbackimage',
            name='image',
            field=models.ImageField(default='not_found.jpg', upload_to='feedbacks', verbose_name='Картинка отзыва'),
        ),
        migrations.AlterField(
            model_name='orderfeedback',
            name='overallPoint',
            field=models.IntegerField(verbose_name='Оценка заказа'),
        ),
        migrations.AlterField(
            model_name='restaurantfeedback',
            name='overallPoint',
            field=models.IntegerField(verbose_name='Общее впечателение о ресторане'),
        ),
    ]
