from django.urls import path

from . import views

urlpatterns = [
    path('index', views.index),
    path('record', views.recordAndDraw),
    path('draw_objects', views.draw_objects),
]
