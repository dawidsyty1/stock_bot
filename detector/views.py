from .models import BearDetect
from django.db.models import Count
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
                'name': item.name,
                'symbol': item.symbol,
                'time': item.time,
            }
            for item in BearDetect.objects.all().order_by('-time')[:20]
        ]

    def get(self, request):
        return Response({
            'bears_list': self.create_bear_list(),
            'most_active_items': self.create_context_for_item()
        })