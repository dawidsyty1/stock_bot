from . import views
from django.urls import path

urlpatterns = [
    path('', views.BearListView.as_view()),
    path(r'csv_data/', views.CSVDataView.as_view()),
]
