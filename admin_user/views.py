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
                'product_id': shoe.id,
                'name': shoe.name,
                'total_quantity':shoe.total_quantity or 0,
                'color': shoe.color.name,
                'price':f"{shoe.price:,.0f}",
                'image_url': image_url
                
                
            })
        print(products)
        
        return render(request, 'admin/Inventory.html', {'products': products})
    
def get_product_detail(request, pk):
    try:
        shoe = Shoe.objects.prefetch_related('sizes').get(pk=pk)
        sizes = shoe.sizes.all().values('size', 'stock')
        data = {
            'product_id': shoe.id,
            'name': shoe.name,
            'price': float(shoe.price),
            'image_url': shoe.images.first().image_url.url if shoe.images.first() else "media/default-shoe.jpg",
            'sizes': list(sizes)
        }
        return JsonResponse(data)
    except Shoe.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)

@csrf_exempt
def update_product(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data['product_id']
        new_price = data['price']
        sizes_data = data['sizes']
        # Cập nhật giá và số lượng
        try:
            shoe = Shoe.objects.get(pk=product_id)
            shoe.price = new_price
            shoe.save()
            for size_data in sizes_data:
                size_obj = ShoeSize.objects.get(shoe=shoe, size=size_data['size'])
                size_obj.stock = size_data['stock']
                size_obj.save()
            return JsonResponse({'status': 'ok'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)
