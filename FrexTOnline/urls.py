"""FrexTOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from FrexTOnline import views

urlpatterns = [
    path('', views.home),
    path('admin/', admin.site.urls),
    path('home/', include('Home.urls')),
    path('login/', include('Login.urls')),
    path('experiment/', include('Experiment.urls')),
    path('file/', include('File.urls')),
    path('course/', include('Course.urls')),
    path('class/', include('Class.urls')),
    path('resource/', views.resource),

    # path('help/', include('Help.urls')),
    # path('resource/', include('Resource.urls')),
    # path('test/', include('Test.urls')),

    path('test/', views.test),
    path('favicon.ico/',views.favicon),
]
