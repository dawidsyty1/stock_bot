from django.db import models
from django.contrib import admin


class TimeResolutions:
    time_divide_values = {
        '1': 15,
        '5': 3,
        '15': 1,
    }

    def time_divide(self, time):
        return self.time_divide_values[time]

    CHOICES = (
            ('1', '1 Minutes'),
            ('5', '5 Minutes'),
            ('15', '15 Minutes'),
            ('15', '15 Minutes'),
        )


class StockType(object):
    STOCK = '1'
    FOREX = '2'
    CRYPTO = '3'

    CHOICES = (
        ('1', 'Stock'),
        ('2', 'Forex'),
        ('3', 'Crypto'),
    )


class Strategy(models.Model):
    name = models.CharField(
        max_length=50,
        default='',
    )

    entry_rule = models.TextField(
        default='',
    )
    exit_rule = models.TextField(
        default='',
    )

    value = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.name}'


class BotSetting(models.Model):
    name = models.CharField(
        max_length=50,
        default='',
    )

    symbol = models.CharField(
        max_length=50,
        default='',
        blank=True, null=True
    )

    family = models.CharField(
        max_length=50,
        default='',
        blank=True, null=True
    )

    token = models.CharField(
        max_length=50,
        default='',
        blank=True, null=True
    )

    strategy = models.ForeignKey(Strategy, blank=True, null=True, on_delete=models.DO_NOTHING)

    time_from = models.TimeField(blank=True, null=True)
    time_to = models.TimeField(blank=True, null=True)

    stock_type = models.CharField(default='1', max_length=1, choices=StockType.CHOICES)
    enable = models.BooleanField(default=False)
    csv_file = models.FileField(upload_to='documents', default='', blank=True, null=True)
    send_sms = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}: {self.symbol}'


class Trade(models.Model):
    time = models.TimeField(blank=True, null=True)

    bot_setting = models.ForeignKey(BotSetting, blank=True, null=True, on_delete=models.DO_NOTHING)

    price_open = models.FloatField(blank=True, null=True)

    price_close = models.FloatField(blank=True, null=True)

    time_resolution = models.CharField(default=1, max_length=2, choices=TimeResolutions.CHOICES)

    def __str__(self):
        return f'{self.time}: {self.symbol} : {self.volume}'


admin.site.register(Strategy)
admin.site.register(BotSetting)
admin.site.register(Trade)


