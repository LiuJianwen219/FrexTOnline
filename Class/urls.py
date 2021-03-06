from django.conf.urls import url
from django.urls import path

from Class import views

urlpatterns = [
    path('create_class/', views.create_class),
    path('delete_class/', views.delete_class),
    path('add_student/', views.add_student),
    path('get_template_class/', views.get_template_class),
    path('dispatch_experiment/', views.dispatch_experiment),
    path('see_homework_status/', views.see_homework_status),
]

