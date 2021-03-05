from . import views
from django.urls import path

urlpatterns = [
    path('', views.MainView.as_view()),
    path(r'trade_data/', views.trade_data_view),
]
