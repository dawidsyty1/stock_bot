from rest_framework import viewsets, mixins, exceptions, status
from scraper import models, serializers
from django.http import HttpResponse
from rest_framework.response import Response
import os
from django.utils.decorators import method_decorator


class DownloadError(exceptions.APIException):
    pass


class DownloadView(mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    @staticmethod
    def resource_response(resource):
        file_handle = open(resource.path, "rb")
        response = HttpResponse(file_handle, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(os.path.basename(file_handle.name))
        return response

    def retrieve(self, request, pk=None):
        response_message = None
        try:
            resource = models.Resource.objects.get(pk=pk)
            if os.path.exists(resource.path):
                return self.resource_response(resource)
            else:
                response_message = "File not found"
        except Exception as error:
            response_message = error
        return Response({'Error': str(response_message)}, status=status.HTTP_404_NOT_FOUND)


class ResourcesView(mixins.DestroyModelMixin, mixins.ListModelMixin,
                    mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = models.Resource.objects.all()
    serializer_class = serializers.ResourcesListSerializer


class TasksView(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin,
                mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = models.Task.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return serializers.TasksListSerializer
        return serializers.TaskSerializer
