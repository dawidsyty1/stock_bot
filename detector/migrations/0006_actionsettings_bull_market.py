# Generated by Django 2.1 on 2020-09-15 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detector', '0005_beardetect_time_resolution'),
    ]

    operations = [
        migrations.AddField(
            model_name='actionsettings',
            name='bull_market',
            field=models.BooleanField(default=False),
        ),
    ]