from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from app.models import Shoe, ShoeImage, ShoeSize, Color, SoleType, Brand
import json
from django.db import transaction
from .services import upload_to_firebase

# Create your views here.
@login_required
@csrf_exempt
def admin_dashboard(request):
    return render(request, 'admin/admin.html')


@login_required
@csrf_exempt
def create_product(request):
    if request.method == 'GET':
        return render(request, 'admin/CreateProduct.html')
    
    if request.method =='POST':
        try:
            with transaction.atomic():
                brand = request.POST.get('brand')
                color = request.POST.get('color')
                sole_type = request.POST.get('sole')
                sizes = request.POST.get('sizes')
                # quantity = request.POST.get('quantity')
                price = request.POST.get('price')
                images = request.FILES.getlist('images')
                sizesJson = json.loads(sizes)

                for key, value in sizesJson.items():
                    print(f"Size: {key}, Quantity: {value}")

                # Tạo sản phẩm mới
                print(brand, color, sole_type, sizesJson, price, images)
        except Exception as e:
            print("Error:", str(e))


        return JsonResponse({'status': 'ok'}, status=200)
    return JsonResponse({'status': 'ok'}, status=200)
    
    
    