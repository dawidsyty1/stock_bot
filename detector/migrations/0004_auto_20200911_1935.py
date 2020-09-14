# Generated by Django 2.1 on 2020-09-11 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detector', '0003_auto_20200911_0921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beardetect',
            name='max_volume',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='beardetect',
            name='price_close',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='beardetect',
            name='price_open',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='beardetect',
            name='volume',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
