from django.conf.urls import url
from django.urls import path

from Course import views

urlpatterns = [
    path('create_template/', views.create_template),
    path('delete_template/', views.delete_template),
    path('create_experiment/', views.create_experiment),
    path('delete_experiment/', views.delete_experiment),
]

