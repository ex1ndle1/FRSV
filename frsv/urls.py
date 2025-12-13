from django.contrib import admin
from django.urls import path
from .views import register,users_info


app_name = 'frsv'
urlpatterns = [
    path('register/', register, name='register'),
    path('users_info/', users_info , name='info')
]