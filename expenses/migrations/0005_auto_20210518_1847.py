# Generated by Django 2.2 on 2021-05-18 23:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0004_auto_20210518_1843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='spend_date',
            field=models.DateField(default=datetime.date(2021, 5, 18)),
        ),
    ]
