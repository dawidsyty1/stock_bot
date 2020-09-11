from django.db import models
from django.contrib import admin

RESOLUTION_CHOICES = (
        ('1', '1 Minutes'),
        ('5', '5 Minutes'),
        ('15', '15 Minutes'),
        ('30', '30 Minutes'),
        ('60', '60 Minutes'),
        ('D', 'Day'),
        ('W', 'Week'),
        ('M', 'Month'),
    )


class ActionSettings(models.Model):
    name = models.CharField(
        max_length=20,
        default='',
    )

    symbol = models.CharField(
        max_length=20,
        default='',
    )

    family = models.CharField(
        max_length=20,
        default='',
    )

    token = models.CharField(
        max_length=50,
        default='',
    )

    volume_percenage = models.IntegerField(default=0)

    price_percenage = models.IntegerField(default=0)

    time_resolution = models.CharField(default=1, max_length=2, choices=RESOLUTION_CHOICES)
    time_from = models.TimeField(blank=True, null=True)
    time_to = models.TimeField(blank=True, null=True)

    enable = models.BooleanField()

    def __str__(self):
        return f'{self.name}: {self.symbol}'


class BearDetect(models.Model):
    symbol = models.CharField(
        max_length=20,
        default='',
    )

    time = models.TimeField(blank=True, null=True)

    volume = models.FloatField()

    max_volume = models.FloatField()

    price_open = models.FloatField()

    price_close = models.FloatField()

    price_percenage = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.time}: {self.symbol} : {self.volume}'


admin.site.register(ActionSettings)
admin.site.register(BearDetect)
