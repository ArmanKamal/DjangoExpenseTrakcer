# Generated by Django 2.2 on 2021-05-02 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='alias',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='countries',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
