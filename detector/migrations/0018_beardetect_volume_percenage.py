# Generated by Django 2.1 on 2020-10-02 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detector', '0017_beardetect_action_settings'),
    ]

    operations = [
        migrations.AddField(
            model_name='beardetect',
            name='volume_percenage',
            field=models.IntegerField(default=0),
        ),
    ]