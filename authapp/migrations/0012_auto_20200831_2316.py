# Generated by Django 3.1 on 2020-08-31 20:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0011_auto_20200831_2315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 2, 23, 16, 10, 631672)),
        ),
    ]
