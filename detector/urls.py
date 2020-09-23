from . import views
from django.urls import path

urlpatterns = [
    path('', views.BearListView.as_view(), name=''),
]
