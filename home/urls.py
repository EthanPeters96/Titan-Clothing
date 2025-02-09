from django.contrib import admin # noqa
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
]
