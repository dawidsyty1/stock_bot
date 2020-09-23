from . import views
from django.urls import path

urlpatterns = [
    path('', views.BearListView.as_view(), name=''),
    path('clear_data', views.BearListView.as_view(), name='clear_data'),
]
