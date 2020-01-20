from rest_framework.routers import DefaultRouter

from scraper import views
from django.urls import path, include

router = DefaultRouter()

router.register(r'scraper/download', views.DownloadView, 'download-test')
router.register(r'scraper/tasks', views.TasksView, 'tasks')
router.register(r'scraper/resources', views.ResourcesView, 'resources')

urlpatterns = router.urls

urlpatterns += [
    path('scraper/download', views.DownloadView.as_view({'get': 'retrieve'}), name='download')
]
