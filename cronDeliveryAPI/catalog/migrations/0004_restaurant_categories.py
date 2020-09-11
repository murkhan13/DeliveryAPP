# Generated by Django 3.0.8 on 2020-07-19 14:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20200718_1153'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='categories',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='categories', to='catalog.Category'),
        ),
    ]
