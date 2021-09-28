from django.conf.urls import url
from django.urls import path

from Experiment import views

urlpatterns = [
    path('newFreeExpProject/', views.create_free_project),
]

