from django.conf.urls import url
from django.urls import path

from Experiment import views

urlpatterns = [
    path('newFreeExpProject/', views.create_free_project),
    path('deleteFreeExpProject/', views.delete_free_project),
    path('free_compile/', views.free_compile),
    path('course_compile/', views.course_compile),
    path('compile_result/', views.compile_result),
    path('experiment/', views.experiment),
]

