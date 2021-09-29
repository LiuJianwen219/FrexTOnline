from django.conf.urls import url
from django.urls import path

from File import views

urlpatterns = [
    # path('introduce/', views.introduce),
    path('uploadfreeexpfile/', views.upload_free_file),
    path('deletefreefile/', views.delete_free_file),
    url(r'downloadfreefile/(?P<f_uid>.+)/', views.download_free_file),
    path('upload_bit/', views.upload_bit),
    path('upload_course/', views.upload_course),
    path('delete_course/', views.delete_course),
    path('upload_homework/', views.upload_homework),
    path('delete_homework/', views.delete_homework),
]

