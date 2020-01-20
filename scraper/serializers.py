import logging
from rest_framework import serializers
from scraper import models, tasks
from scraper.validators import validate_url_address
from django.urls import reverse


class ResourcesListSerializer(serializers.ModelSerializer):
    """
    Serializer for the Resources objects list.
    """
    download_url = serializers.SerializerMethodField()

    class Meta:
        model = models.Resource
        fields = '__all__'

    def get_download_url(self, obj):
        """
        Build download url as JSON response.
        """
        absolute_url = self.context['request'].build_absolute_uri(location=reverse('download'))
        return obj.build_download_url(absolute_url)


class TasksListSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task objects list.
    """
    download_urls = serializers.SerializerMethodField()

    class Meta:
        model = models.Task
        fields = '__all__'

    def get_download_urls(self, obj):
        """
        Build download urls as JSON response.
        """
        resources = models.Resource.objects.filter(task=obj.pk)

        absolute_url = self.context['request'].build_absolute_uri(
            location=reverse('download')
        )

        response = {
            content.file_name: content.build_download_url(absolute_url)
            for content in resources
        }

        return response


class TaskSerializer(serializers.ModelSerializer):
    """
     Serializer for the Task objects.
     """
    url = serializers.CharField(required=True, validators=[validate_url_address])

    class Meta:
        model = models.Task
        fields = ('url', 'type')

    def create(self, validated_data):
        task = models.Task.objects.create(**validated_data)
        task.set_as_new()
        tasks.start_new_task(task.id)
        return task
