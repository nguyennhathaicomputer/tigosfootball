from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from app.models import Shoe, ShoeImage, ShoeSize, Color, SoleType, Brand
import json
from django.db import transaction
from .services import upload_to_firebase
from decimal import Decimal, InvalidOperation
from django.db.models import Sum
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
                brand_name = request.POST.get('brand')
                color = request.POST.get('color')
                sole_type = request.POST.get('sole')
                sizes = request.POST.get('sizes')
                # quantity = request.POST.get('quantity')
                price = request.POST.get('price')
                images = request.FILES.getlist('images')
                sizesJson = json.loads(sizes)

                brand = Brand.objects.create(name=brand_name)
                sole = SoleType.objects.create(name=sole_type, brand=brand)
                color = Color.objects.create(name=color)
                price_insert = Decimal(price)
                
                shoe = Shoe.objects.create(
                    name = brand_name,
                    brand=brand,
                    sole_type = sole,
                    color = color,
                    price = price_insert,
                    description = "test des"
                     
                )
                
                for f in images:
                    shoeImage = ShoeImage.objects.create(
                        image_url = f,
                        shoe=shoe
                    )
                    shoeImage.save()
                
                for key, value in sizesJson.items():
                    shoeSize = ShoeSize.objects.create(
                        shoe = shoe,
                        size =key,
                        stock = value
                    )
                    shoeSize.save()
                # Tạo sản phẩm mới
        except Exception as e:
            return JsonResponse({
                'message': e
            }, status=500)


        return JsonResponse({'status': 'ok'}, status=200)
    return JsonResponse({'status': 'ok'}, status=200)
    
    
@login_required
@csrf_exempt
def inventory(request):
    if request.method =='GET':
        
        shoes = Shoe.objects.annotate(
            total_quantity = Sum('sizes__stock')
        ).prefetch_related('images').all()
        
        products = []
        for shoe in shoes:
            first_image = shoe.images.first()
            image_url = first_image.image_url.url if first_image else "media/default-shoe.jpg"
            products.append({
                'name': shoe.name,
                'total_quantity':shoe.total_quantity or 0,
                'color': shoe.color.name,
                'price':f"{shoe.price:,.0f}",
                'image_url': image_url
                
                
            })
        print(products)
        
        return render(request, 'admin/Inventory.html', {'products': products})
    
