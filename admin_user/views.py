from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from app.models import Brand, Color, SoleType, Shoe, Size, ShoeVariant, ShoeImage
import json
from django.db import transaction
from .services import upload_to_firebase
from decimal import Decimal, InvalidOperation
from django.db.models import Sum
from django.db.models import F

# Create your views here.
@login_required
@csrf_exempt
def admin_dashboard(request):
    return render(request, 'admin/admin.html')


# @login_required
# @csrf_exempt
# def create_product(request):
#     if request.method == 'GET':
#         return render(request, 'admin/CreateProduct.html')
    
#     if request.method =='POST':
#         try:
#             with transaction.atomic():
#                 brand_name = request.POST.get('brand')
#                 color = request.POST.get('color')
#                 name = request.POST.get('name')
#                 sole_type = request.POST.get('sole')
#                 sizes = request.POST.get('sizes')
#                 # quantity = request.POST.get('quantity')
#                 price = request.POST.get('price')
#                 images = request.FILES.getlist('images')
#                 sizesJson = json.loads(sizes)

#                 brand = Brand.objects.create(name=brand_name)
#                 sole = SoleType.objects.create(name=sole_type, brand=brand)
#                 color = Color.objects.create(name=color)
#                 price_insert = Decimal(price)
                
#                 shoe = Shoe.objects.create(
#                     name = name,
#                     brand=brand,
#                     sole_type = sole,
#                     color = color,
#                     price = price_insert,
#                     description = "test des"
                     
#                 )
                
#                 for f in images:
#                     shoeImage = ShoeImage.objects.create(
#                         image_url = f,
#                         shoe=shoe
#                     )
#                     shoeImage.save()
                
#                 for key, value in sizesJson.items():
#                     shoeSize = ShoeSize.objects.create(
#                         shoe = shoe,
#                         size =key,
#                         stock = value
#                     )
#                     shoeSize.save()
#                 # Tạo sản phẩm mới
#         except Exception as e:
#             return JsonResponse({
#                 'message': e
#             }, status=500)


#         return JsonResponse({'status': 'ok'}, status=200)
#     return JsonResponse({'status': 'ok'}, status=200)



@login_required
@csrf_exempt
def create_product(request):
    if request.method == 'GET':
        return render(request, 'admin/CreateProduct.html')
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Lấy dữ liệu từ request
                brand_name = request.POST.get('brand')
                color_name = request.POST.get('color')
                shoe_name = request.POST.get('name')
                price_str = request.POST.get('price')
                variants_json = request.POST.get('variants')
                images = request.FILES.getlist('images')

                # Kiểm tra dữ liệu bắt buộc
                if not all([brand_name, color_name, shoe_name, price_str, variants_json]):
                    return JsonResponse({'status': 'error', 'message': 'Thiếu thông tin bắt buộc'}, status=400)

                # Parse variants
                try:
                    variants_data = json.loads(variants_json)
                    if not isinstance(variants_data, list):
                        raise ValueError
                except:
                    return JsonResponse({'status': 'error', 'message': 'Dữ liệu variants không hợp lệ'}, status=400)

                # Gom nhóm các variant theo (size, sole_name) để tránh trùng lặp và cộng dồn số lượng
                variant_dict = {}
                for v in variants_data:
                    size = v.get('size')
                    sole_name = v.get('sole_name')
                    quantity = v.get('quantity')
                    if not size or not sole_name or not quantity:
                        return JsonResponse({'status': 'error', 'message': 'Mỗi variant phải có size, sole_name và quantity'}, status=400)
                    key = (size, sole_name)
                    variant_dict[key] = variant_dict.get(key, 0) + int(quantity)

                # Xử lý Brand, Color (get_or_create)
                # brand, _ = Brand.objects.get_or_create(name=brand_name)
                brand = Brand.objects.filter(name__iexact = brand_name).first()
                if not brand:
                    brand = Brand.objects.create(name=brand_name)
                color, _ = Color.objects.get_or_create(name=color_name)

                # Xử lý giá
                try:
                    price = Decimal(price_str)
                except:
                    return JsonResponse({'status': 'error', 'message': 'Giá không hợp lệ'}, status=400)

                # Tạo Shoe
                shoe = Shoe.objects.create(
                    name=shoe_name,
                    brand=brand,
                    color=color,
                    price=price,
                    description=""
                )

                # Xử lý ảnh
                for f in images:
                    ShoeImage.objects.create(shoe=shoe, image_url=f)

                # Xử lý variants
                for (size_name, sole_name), total_stock in variant_dict.items():
                    # Lấy hoặc tạo Size
                    size_obj, _ = Size.objects.get_or_create(name=size_name)

                    # Lấy hoặc tạo SoleType (phải gắn với brand)
                    sole_obj = SoleType.objects.filter(name__iexact=sole_name).first()
                    # sole_obj, _ = SoleType.objects.get_or_create(
                    #     name=sole_name,
                    # )
                    if not sole_obj:
                        sole_obj = SoleType.objects.create(name=sole_name)

                    # Kiểm tra ShoeVariant đã tồn tại chưa
                    variant, created = ShoeVariant.objects.get_or_create(
                        shoe=shoe,
                        size=size_obj,
                        soleType=sole_obj,
                        defaults={'stock': total_stock}
                    )

                    if not created:
                        # Nếu đã tồn tại, cộng dồn stock
                        variant.stock = F('stock') + total_stock
                        variant.save(update_fields=['stock'])

                return JsonResponse({'status': 'ok'}, status=200)

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)

    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)
    
    
# @login_required
# @csrf_exempt
# def inventory(request):
#     if request.method =='GET':
        
#         shoes = Shoe.objects.annotate(
#             total_quantity = Sum('sizes__stock')
#         ).prefetch_related('images').all()
        
#         products = []
#         for shoe in shoes:
#             first_image = shoe.images.first()
#             image_url = first_image.image_url.url if first_image else "media/default-shoe.jpg"
#             products.append({
#                 'product_id': shoe.id,
#                 'name': shoe.name,
#                 'total_quantity':shoe.total_quantity or 0,
#                 'color': shoe.color.name,
#                 'price':f"{shoe.price:,.0f}",
#                 'image_url': image_url
                
                
#             })
#         print(products)
        
#         return render(request, 'admin/Inventory.html', {'products': products})

@login_required
@csrf_exempt
def inventory(request):
    if request.method == 'GET':
        shoes = Shoe.objects.annotate(
            total_quantity=Sum('variants__stock')
        ).select_related('color').prefetch_related('images').all()

        products = []
        for shoe in shoes:
            first_image = shoe.images.first()
            image_url = first_image.image_url.url if first_image else "media/default-shoe.jpg"
            products.append({
                'product_id': shoe.id,
                'name': shoe.name,
                'total_quantity': shoe.total_quantity or 0,
                'color': shoe.color.name,
                'price': f"{shoe.price:,.0f}",
                'image_url': image_url
            })
        return render(request, 'admin/Inventory.html', {'products': products})
    
# def get_product_detail(request, pk):
#     try:
#         shoe = Shoe.objects.prefetch_related('sizes').get(pk=pk)
#         sizes = shoe.sizes.all().values('size', 'stock')
#         data = {
#             'product_id': shoe.id,
#             'name': shoe.name,
#             'price': float(shoe.price),
#             'image_url': shoe.images.first().image_url.url if shoe.images.first() else "media/default-shoe.jpg",
#             'sizes': list(sizes)
#         }
#         return JsonResponse(data)
#     except Shoe.DoesNotExist:
#         return JsonResponse({'error': 'Not found'}, status=404)


# def get_product_detail(request, pk):
#     try:
#         shoe = Shoe.objects.prefetch_related('images', 'variants__size').get(pk=pk)
#         # Nhóm các variant theo size và tính tổng stock
#         size_stock = {}
#         for variant in shoe.variants.all():
#             size_name = variant.size.name
#             size_stock[size_name] = size_stock.get(size_name, 0) + variant.stock

#         # Chuyển thành list các dict giống cấu trúc cũ
#         sizes = [{'size': k, 'stock': v} for k, v in size_stock.items()]

#         first_image = shoe.images.first()
#         image_url = first_image.image_url.url if first_image else "media/default-shoe.jpg"

#         data = {
#             'product_id': shoe.id,
#             'name': shoe.name,
#             'price': float(shoe.price),
#             'image_url': image_url,
#             'sizes': sizes
#         }
#         return JsonResponse(data)
#     except Shoe.DoesNotExist:
#         return JsonResponse({'error': 'Not found'}, status=404)

@login_required
@csrf_exempt
def get_product_detail(request, pk):
    try:
        shoe = Shoe.objects.prefetch_related('images', 'variants__size', 'variants__soleType').get(pk=pk)
        variants = []
        for variant in shoe.variants.all():
            variants.append({
                'size': variant.size.name,
                'sole': variant.soleType.name,
                'stock': variant.stock
            })
        first_image = shoe.images.first()
        image_url = first_image.image_url.url if first_image else "/media/default-shoe.jpg"
        data = {
            'product_id': shoe.id,
            'name': shoe.name,
            'price': float(shoe.price),
            'image_url': image_url,
            'variants': variants  # thay vì sizes
        }
        return JsonResponse(data)
    except Shoe.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)

# @csrf_exempt
# def update_product(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         product_id = data['product_id']
#         new_price = data['price']
#         sizes_data = data['sizes']
#         # Cập nhật giá và số lượng
#         try:
#             shoe = Shoe.objects.get(pk=product_id)
#             shoe.price = new_price
#             shoe.save()
#             for size_data in sizes_data:
#                 size_obj = ShoeSize.objects.get(shoe=shoe, size=size_data['size'])
#                 size_obj.stock = size_data['stock']
#                 size_obj.save()
#             return JsonResponse({'status': 'ok'})
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)
#     return JsonResponse({'error': 'Method not allowed'}, status=405)


@login_required
@csrf_exempt
def update_product(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            new_price = data.get('price')
            variants_data = data.get('variants')  # list of {size, sole, stock}

            shoe = Shoe.objects.get(pk=product_id)

            with transaction.atomic():
                # Cập nhật giá nếu có
                if new_price is not None:
                    shoe.price = Decimal(new_price)
                    shoe.save()

                # Cập nhật stock cho từng variant
                for v in variants_data:
                    size_name = v.get('size')
                    sole_name = v.get('sole')
                    stock = v.get('stock', 0)

                    # Lấy size và sole (phải tồn tại)
                    size_obj = Size.objects.get(name=size_name)
                    sole_obj = SoleType.objects.get(name=sole_name, brand=shoe.brand)

                    # Cập nhật stock (dùng update_or_create để an toàn, nhưng nếu không tồn tại thì tạo mới? Có thể không cho phép tạo mới)
                    # Ở đây ta giả sử chỉ cập nhật variant đã tồn tại, nếu không thì bỏ qua hoặc báo lỗi
                    try:
                        variant = ShoeVariant.objects.get(shoe=shoe, size=size_obj, soleType=sole_obj)
                        variant.stock = stock
                        variant.save()
                    except ShoeVariant.DoesNotExist:
                        # Có thể log hoặc bỏ qua
                        pass

                return JsonResponse({'status': 'ok'})
        except Shoe.DoesNotExist:
            return JsonResponse({'error': 'Shoe not found'}, status=404)
        except (Size.DoesNotExist, SoleType.DoesNotExist) as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Method not allowed'}, status=405)
