from . import views
from django.urls import path

urlpatterns = [
    path('', views.MainView.as_view()),
]
