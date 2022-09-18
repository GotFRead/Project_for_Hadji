"""Application URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, re_path
from user_site_part import views

urlpatterns = [
    path('', views.authorization, name='authorization'),
    path('test/', views.test, name='test'),
    path('main/', views.main_user_form, name='main_form_user'),
    path('admin/', admin.site.urls, name='admin'),
    path('registration/', views.registration, name='registration'),
    path('choose_main_form/', views.choose_main_form, name='choose_main_form'),
    re_path(r'^create_visit/(?P<ser_pk>\d+)/(?P<s_pk>\d+)', views.create_an_appointment, name='create_visit'),
    re_path(r'^details/(?P<pk>\d+)$', views.service_details, name='service-details'),
    #path('create_appointment', views.create_an_appointment, name='create_appointment')
]
