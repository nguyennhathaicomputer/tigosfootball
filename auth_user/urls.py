from django.contrib import admin
from django.urls import path
from .views import login_view, register, logout_view

app_name = 'auth_user'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout_view, name='logout'),
]
