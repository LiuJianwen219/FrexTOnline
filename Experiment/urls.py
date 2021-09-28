from django.conf.urls import url
from django.urls import path

from Experiment import views

urlpatterns = [
    path('newFreeExpProject/', views.create_free_project),
    path('deleteFreeExpProject/', views.delete_free_project),
    path('freecompile/', views.free_compile),
    path('compile_result/', views.compile_result),
    path('experiment/', views.experiment),
]

