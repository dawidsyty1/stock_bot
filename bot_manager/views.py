from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from .fetcher import grab_data
from .models import BotSetting


class MainView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'main_view.html'

    def get(self, request):
        remove_action = request.GET.get('start_task', 'false')
        if remove_action == 'true':
            for item in BotSetting.objects.filter(enable=True):
                grab_data(item)
        return Response()
