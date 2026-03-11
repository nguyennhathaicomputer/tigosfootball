from django.contrib import admin
from django.urls import path
from django.urls import include
from .views import admin_dashboard, create_product, inventory,get_product_detail,update_product

app_name = 'admin_user'

urlpatterns = [
    path('dashboard/', admin_dashboard, name='dashboard'),
    path('products/', create_product, name='create_product'),
    path('inventory/', inventory, name = 'inventory'),
    path('api/product/<int:pk>/', get_product_detail, name='product-detail'),
    path('api/update-product/', update_product, name='update-product'),
    
]
