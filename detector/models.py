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

    volume_percenage = models.IntegerField(default=0)

    price_percenage = models.IntegerField(default=0)

    time_resolution = models.CharField(default=1, max_length=2, choices=TimeResolutions.CHOICES)
    time_from = models.TimeField(blank=True, null=True)
    time_to = models.TimeField(blank=True, null=True)
    stock_type = models.CharField(default='1', max_length=1, choices=StockType.CHOICES)
    enable = models.BooleanField(default=False)
    bull_market = models.BooleanField(default=False)
    forced = models.BooleanField(default=False)
    csv_file = models.FileField(upload_to='documents', default='', blank=True, null=True)

    def __str__(self):
        return f'{self.name}: {self.symbol}'


class BearDetect(models.Model):
    symbol = models.CharField(
        max_length=50,
        default='',
    )

    name = models.CharField(
        max_length=50,
        default='',
    )

    time = models.TimeField(blank=True, null=True)

    volume = models.FloatField(blank=True, null=True)

    max_volume = models.FloatField(blank=True, null=True)

    price_open = models.FloatField(blank=True, null=True)

    time_resolution = models.CharField(default=1, max_length=2, choices=TimeResolutions.CHOICES)

    price_close = models.FloatField(blank=True, null=True)

    price_percenage = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.time}: {self.symbol} : {self.volume}'


class BearDetectAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol', 'time', 'volume', 'max_volume', 'price_open', 'price_close', 'price_percenage')
    readonly_fields = ('name', 'symbol', 'time', 'volume', 'max_volume', 'price_open', 'price_close')


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


def set_percentage_volument_100_action(modeladmin, request, queryset):
    queryset.update(volume_percenage=100)
    short_description = "Set percentage volument 100"


def set_percentage_volument_130_action(modeladmin, request, queryset):
    queryset.update(volume_percenage=130)
    short_description = "Set percentage volument 100"


def set_percentage_volument_150_action(modeladmin, request, queryset):
    queryset.update(volume_percenage=150)
    short_description = "Set percentage volument 100"


def set_percentage_volument_200_action(modeladmin, request, queryset):
    queryset.update(volume_percenage=200)
    short_description = "Set percentage volument 200"


def enable_bull_market_action(modeladmin, request, queryset):
    queryset.update(bull_market=True)
    short_description = "Enable bull market"


def disable_bull_market_action(modeladmin, request, queryset):
    queryset.update(bull_market=False)
    short_description = "Disable bull market"


def clear_tokens(modeladmin, request, queryset):
    queryset.update(token='')
    short_description = "Clear all tokens"


def set_time_1_action(modeladmin, request, queryset):
    queryset.update(time_resolution='1')
    short_description = "set_time_1_action"


def set_time_5_action(modeladmin, request, queryset):
    queryset.update(time_resolution='5')
    short_description = "set_time_5_action"


def set_time_15_action(modeladmin, request, queryset):
    queryset.update(time_resolution='15')
    short_description = "set_time_15_action"


def set_time_60_action(modeladmin, request, queryset):
    queryset.update(time_resolution='60')
    short_description = "set_time_60_action"


class ActionSettingsAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name',
        'symbol', 'stock_type',
        'volume_percenage', 'price_percenage',
        'token', 'time_resolution',
        'enable', 'bull_market',
        'csv_file'
    )
    actions = [
        disable_action,
        enable_action,
        set_time_1_action,
        set_time_5_action,
        set_time_15_action,
        set_time_60_action,
        set_percentage_volument_70_action,
        set_percentage_volument_10_action,
        set_percentage_volument_50_action,
        set_percentage_volument_100_action,
        set_percentage_volument_130_action,
        set_percentage_volument_150_action,
        set_percentage_volument_200_action,
        clear_tokens
    ]
    search_fields = ('id', 'name', 'symbol')

    list_filter = ('stock_type', 'time_resolution', 'enable', 'bull_market', 'forced')


admin.site.register(ActionSettings, ActionSettingsAdmin)
admin.site.register(BearDetect, BearDetectAdmin)
