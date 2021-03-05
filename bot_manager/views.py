from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from .fetcher import grab_data
from .parser import parse_item, parse_trade
from .models import BotSetting, Trade
from .tasks import task_make_backtest
from django.shortcuts import redirect

class MainView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'main_view.html'

    def get(self, request):
        start_task = request.GET.get('start_task', 'false')
        if start_task == 'true':
            for item in BotSetting.objects.filter(enable=True):
                grab_data(item)
            return redirect('/')

        parse_task = request.GET.get('parse_task', 'false')
        if parse_task == 'true':
            for item in BotSetting.objects.filter(enable=True):
                parse_item(item)
            return redirect('/')

        p_trade = request.GET.get('parse_trade', 'false')
        if p_trade == 'true':
            for item in Trade.objects.all():
                parse_trade(item)
            return redirect('/')

        start_backtest = request.GET.get('start_backtest', 'false')
        if start_backtest == 'true':
            task_make_backtest.apply_async()
            return redirect('/')

        clear_data = request.GET.get('clear_data', 'false')
        if clear_data == 'true':
            Trade.objects.all().delete()
            return redirect('/')
        return Response()


def create_trade_list():
    trade_items = Trade.objects.all()
    return [
        {
            'datetime_entry_rule': item.datetime_entry_rule,
            'datetime_entry': item.datetime_entry,
            'datetime_exist': item.datetime_exist,
            'datetime_exit_rule': item.datetime_exit_rule,
            'bot_setting_name': item.bot_setting.name,
            'bot_setting_symbol': item.bot_setting.symbol,
            'price_open': item.price_open,
            'price_close': item.price_close,
        }
        for item in trade_items
    ]


def trade_data_view(request):
    trade_list = create_trade_list()
    data = {
        'trade_list': trade_list,
    }

    return JsonResponse(data)
