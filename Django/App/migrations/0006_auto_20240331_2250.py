# Generated by Django 3.2.13 on 2024-03-31 22:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0005_auto_20240312_1017'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='Size',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='order',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 31, 22, 50, 18, 890298)),
        ),
    ]