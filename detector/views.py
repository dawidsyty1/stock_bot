from .models import BearDetect
from django.db.models import Count
from django.shortcuts import redirect
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView



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
            for item in queryset.values('name').annotate(c=Count('name')).order_by('-c')
        ]

    @staticmethod
    def create_bear_list():
        return [
            {
                'action_settings': item.action_settings.id,
                'name': item.name,
                'time': item.time,
                'volume': item.volume,
                'max_volume': item.max_volume,
                'price_open': item.price_open,
                'price_close': item.price_close,
                'price_percenage': item.price_percenage,
            }
            for item in BearDetect.objects.all().order_by('-time')[:20]
        ]

    def get(self, request):
        if request.GET.get('clear_data', 'false') == 'true':
            BearDetect.objects.all().delete()
            return redirect('/')
        return Response({
            'bears_list': self.create_bear_list(),
            'most_active_items': self.create_context_for_item()
        })