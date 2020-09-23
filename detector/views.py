from .models import BearDetect
import csv
from django.db.models import Count
from django.shortcuts import redirect
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from .tasks import task_clean_up_and_set_data, task_us_get_data, task_delete_all_data, task_delete_all_action_list


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


class BearListView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'bear_detector.html'

    @staticmethod
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

    @staticmethod
    def create_bear_list():
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
                'csv_file': item.action_settings.csv_file,
            }
            for item in BearDetect.objects.all().order_by('-time')[:20]
        ]

    def get(self, request):
        return Response({
            'bears_list': self.create_bear_list(),
            'most_active_items': self.create_context_for_item()
        })