from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('request_page', views.request_page),
]
