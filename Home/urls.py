from django.conf.urls import url
from django.urls import path, include

from Home import views

urlpatterns = [
    path('', views.home),
    path('introduce/', views.introduce),
    path('experiment/', views.experiment),
]
