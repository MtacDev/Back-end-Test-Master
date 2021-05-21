"""mysite URL Configuration

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
from django.urls import path
from menu import views
from .utils.healthz import healthz
from menu.views import run_task, getUUID 

urlpatterns = [
    path('',views.login, name = 'login'),
    path('home',views.home, name = 'home'),
    path('adminform',views.adminform, name = 'adminform'),
    path('createmenu',views.createMenu, name = 'createmenu'),
    path("healthz", healthz, name="healthz"),
    path("menuoftheday", views.menuoftheday, name="menuoftheday"),
    path("menurequests", views.menurequests, name="menurequests"),
    path("modifymenu", views.modifyMenu, name="modifymenu"),
    path("tasks/", run_task, name="run_task"),
    path("menu/<uuid>/", getUUID, name="getUUID"),
]
