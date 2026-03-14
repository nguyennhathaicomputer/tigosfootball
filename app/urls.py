from django.contrib import admin
from django.urls import path
from .views import home, product_detail

app_name = 'app'

urlpatterns = [
    path('', home, name='home'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
]
