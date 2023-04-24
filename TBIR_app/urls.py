from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name = 'welcome'),
    path('result', views.result, name = 'result')
]