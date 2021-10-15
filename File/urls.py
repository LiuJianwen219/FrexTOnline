from django.conf.urls import url
from django.urls import path

from File import views

urlpatterns = [
    # path('introduce/', views.introduce),
    path('uploadfreeexpfile/', views.upload_free_file),
    path('deletefreefile/', views.delete_free_file),
    url(r'download_free_file/(?P<f_uid>.+)/', views.download_file),
    path('upload_bit/', views.upload_bit),
    path('upload_course/', views.upload_course),
    path('delete_course/', views.delete_course),
    url(r'download_course/(?P<homeworkId>.+)/', views.download_course),
    path('upload_homework/', views.upload_homework),
    path('delete_homework/', views.delete_homework),
    url(r'download_homework/(?P<f_uid>.+)/', views.download_file),
    url(r'download_homework_report/(?P<h_uid>.+)/(?P<file_type>.+)/', views.download_homework_report),

    path('get_experiment_file_content/', views.get_experiment_file_content),
    path('edit_experiment_file/', views.edit_experiment_file),
]

