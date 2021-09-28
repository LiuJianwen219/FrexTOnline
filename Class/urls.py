from django.conf.urls import url
from django.urls import path

from Class import views

urlpatterns = [
    path('create_class/', views.create_class),
    path('add_student/', views.add_student)
]

