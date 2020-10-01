from .models import BearDetect
import csv
from django.db.models import Count
from django.shortcuts import redirect
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from .tasks import task_clean_up_and_set_data, task_us_get_data, task_delete_all_data, task_delete_all_action_list
from django.http import JsonResponse


class CSVDataView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'csv_file_data.html'

    def get(self, request):
        force_clean_up = request.GET.get('force_clean_up', 'false')
        if force_clean_up == 'true':
            task_clean_up_and_set_data.apply_async(args=())
            return redirect('/')

        remove_action = request.GET.get('remove_all_action', 'false')
        if remove_action == 'true':
            task_delete_all_data()
            task_delete_all_action_list()
            return redirect('/')

        force_fetch_data = request.GET.get('force_fetch_data', 'false')
        if force_fetch_data == 'true':
            task_us_get_data.delay()
            return redirect('/')

        if request.GET.get('clear_data', 'false') == 'true':
            BearDetect.objects.all().delete()
            return redirect('/')

        file_name = request.GET.get('file_name', '')
        try:
            reader = csv.reader(open(f'data/{file_name}'))
        except FileNotFoundError:
            return redirect('/')

        hours_dictionary_average = {
            row[0].split(' ')[1]: row[0].split(' ')[2]
            for row in reader
        }
        return Response({
            'csv_datas': hours_dictionary_average,
        })


def create_context_for_item():
    queryset = BearDetect.objects.all()
    return [
        {
            'name': item['name'],
            'count': item['c'],
            'link': f'https://www.etoro.com/markets/{item["name"]}/chart'
        }
        for item in queryset.values('name').annotate(c=Count('name')).order_by('-c')[:10]
    ]


def create_bear_list(show_all):
    bears_items = BearDetect.objects.all().order_by('-time')[:20]
    if show_all:
        bears_items = BearDetect.objects.all().order_by('-time')
    return [
        {
            'action_settings': item.action_settings.id,
            'name': item.name,
            'symbol': item.symbol,
            'link': f'https://www.etoro.com/markets/{item.symbol}/chart',
            'time': item.time,
            'volume': item.volume,
            'max_volume': item.max_volume,
            'price_open': item.price_open,
            'price_close': item.price_close,
            'price_percenage': item.price_percenage,
            'csv_file': str(item.action_settings.csv_file),
        }
        for item in bears_items
    ]


class BearListView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'bear_detector.html'

    def get(self, request):
            show_all = request.GET.get('show_all', 'false')
            bears_list = create_bear_list(show_all == 'true')
            user_id = request.user.id
            return Response({
                'bears_list': bears_list,
                'most_active_items': create_context_for_item(),
                'beat_title': f'{len(bears_list)}: last: {bears_list[0]["time"] if len(bears_list) > 0 else ""}',
                'user_id': user_id
            })


def bear_data_view(request):
    bears_list = create_bear_list(False)
    data = {
        'bears_list': bears_list,
        'most_active_items': create_context_for_item(),
    }

    return JsonResponse(data)
