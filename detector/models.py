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


class StockType(object):
    STOCK = '1'
    FOREX = '2'
    CRYPTO = '3'

    CHOICES = (
        ('1', 'Stock'),
        ('2', 'Forex'),
        ('3', 'Crypto'),
    )


class ActionSettings(models.Model):
    name = models.CharField(
        max_length=50,
        default='',
    )

    symbol = models.CharField(
        max_length=50,
        default='',
    )

    family = models.CharField(
        max_length=50,
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
    stock_type = models.CharField(default='1', max_length=1, choices=StockType.CHOICES)
    enable = models.BooleanField(default=False)
    bull_market = models.BooleanField(default=False)
    csv_file = models.FileField(upload_to='documents', default='')

    def __str__(self):
        return f'{self.name}: {self.symbol}'


class BearDetect(models.Model):
    symbol = models.CharField(
        max_length=20,
        default='',
    )

    time = models.TimeField(blank=True, null=True)

    volume = models.FloatField(blank=True, null=True)

    max_volume = models.FloatField(blank=True, null=True)

    price_open = models.FloatField(blank=True, null=True)

    time_resolution = models.CharField(default=1, max_length=2, choices=RESOLUTION_CHOICES)

    price_close = models.FloatField(blank=True, null=True)

    price_percenage = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.time}: {self.symbol} : {self.volume}'


class BearDetectAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'time', 'volume', 'max_volume', 'price_open', 'price_close')
    readonly_fields = ('symbol', 'time', 'volume', 'max_volume', 'price_open', 'price_close')


def disable_action(modeladmin, request, queryset):
    queryset.update(enable=False)
    short_description = "Disable all"


def enable_action(modeladmin, request, queryset):
    queryset.update(enable=True)
    short_description = "Enable all"


def set_percentage_volument_70_action(modeladmin, request, queryset):
    queryset.update(volume_percenage=70)
    short_description = "Set percentage volument 70"


def set_percentage_volument_10_action(modeladmin, request, queryset):
    queryset.update(volume_percenage=10)
    short_description = "Set percentage volument 10"


def set_percentage_volument_50_action(modeladmin, request, queryset):
    queryset.update(volume_percenage=50)
    short_description = "Set percentage volument 50"


def enable_bull_market_action(modeladmin, request, queryset):
    queryset.update(bull_market=True)
    short_description = "Enable bull market"


def disable_bull_market_action(modeladmin, request, queryset):
    queryset.update(bull_market=False)
    short_description = "Disable bull market"


class ActionSettingsAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol', 'stock_type', 'volume_percenage', 'price_percenage', 'token', 'time_resolution', 'enable', 'bull_market')
    actions = [
        disable_action, enable_action, set_percentage_volument_70_action, set_percentage_volument_10_action, set_percentage_volument_50_action
    ]
    search_fields = ('name', 'symbol')

    list_filter = ('stock_type', 'time_resolution', 'enable', 'bull_market')


admin.site.register(ActionSettings, ActionSettingsAdmin)
admin.site.register(BearDetect, BearDetectAdmin)
