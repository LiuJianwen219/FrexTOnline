from django.conf.urls import url
from django.urls import path

from Experiment import views

urlpatterns = [
    path('newFreeExpProject/', views.create_free_project),
    path('deleteFreeExpProject/', views.delete_free_project),
    path('free_compile/', views.free_compile),
    path('course_compile/', views.course_compile),
    path('get_compile_status/', views.get_compile_status),
    path('compile_result/', views.compile_result),
    path('experiment/', views.experiment_start),
    path('experiment_status/', views.experiment_status),
    path('burn_bit/', views.burn_bit),
    path('burn_bit_status/', views.burn_bit_status),
]
