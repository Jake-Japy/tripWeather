# Generated by Django 5.1.1 on 2024-09-09 15:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tripResultReturnApi', '0006_alter_cityweatherinfo_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cityweatherinfo',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 9, 9, 17, 28, 12, 551931)),
        ),
    ]
