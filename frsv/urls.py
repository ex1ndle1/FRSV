from django.contrib import admin
from django.urls import path
from .views import register



app_name = 'frsv'
urlpatterns = [
    path('register/', register, name='register')
]