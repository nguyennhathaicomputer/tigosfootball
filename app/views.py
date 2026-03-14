from django.shortcuts import render, get_object_or_404
from .models import Shoe, Brand, SoleType, Size

# # Create your views here.
# def home(request):
#     # Lấy tất cả giày, kèm ảnh đầu tiên, giá, màu, brand
#     # if not request.user.is_authenticated:
    
#     shoes = Shoe.objects.prefetch_related('images', 'sizes').select_related('brand', 'color').all()
    
#     # Chuẩn bị dữ liệu để truyền vào template
#     product_list = []
#     for shoe in shoes:
#         first_image = shoe.images.first()
#         image_url = first_image.image_url.url if first_image else '/static/images/default.jpg'
#         # Lấy danh sách size của sản phẩm (dạng chuỗi để gán vào data-attribute)
#         sizes = shoe.sizes.values_list('size', flat=True)
#         sizes_str = ','.join([str(s) for s in sizes])
        
#         product_list.append({
#             'id': shoe.id,
#             'name': shoe.name,
#             'brand': shoe.brand.name,
#             'color': shoe.color.name,
#             'price': float(shoe.price),
#             'image_url': image_url,
#             'sizes': sizes_str,
#         })
    
#     # Lấy tất cả brand để hiển thị checkbox filter (nếu sidebar cần dynamic)
#     brands = Brand.objects.all()
#     # Có thể lấy tất cả size duy nhất từ tất cả giày (nếu cần)
#     # all_sizes = ShoeSize.objects.values_list('size', flat=True).distinct().order_by('size')
#     all_sizes = Size.objects.all()
#     soleType = SoleType.objects.values('name').distinct()
    
#     context = {
#         'products': product_list,
#         'brands': brands,
#         'sizes': all_sizes,
#         'soleTypes': soleType
#     }
#     return render(request, 'base.html', context)


def home(request):
    # Lấy tất cả giày, kèm theo ảnh đầu tiên, brand, color, và các variants + size liên quan
    shoes = Shoe.objects.prefetch_related(
        'images',
        'variants__size',          # Prefetch variants và size của variants
        'variants__soleType'
    ).select_related('brand', 'color').all()
    
    print(shoes)

    product_list = []
    for shoe in shoes:
        # Lấy ảnh đầu tiên (nếu có)
        first_image = shoe.images.first()
        image_url = first_image.image_url.url if first_image else '/static/images/default.jpg'

        # Lấy danh sách size name từ tất cả variants của giày (loại bỏ trùng lặp)
        size_names = set()
        sole_names = set()
        for variant in shoe.variants.all():
            size_names.add(variant.size.name)   # variant.size là ForeignKey tới Size
            sole_names.add(variant.soleType.name)
            
        # sole_names =set()
        # for variant in shoe.variants.all():
        #     sole_names.add(variant.soleType.name)
        # soles_str = ', '.join(sole_names)
        # sole_names = set()
        # sole_names.add(shoe.variants.soleType.name)
        # soles_str = ','.join(sole_names)
        

        # Sắp xếp size (nếu là số) và nối thành chuỗi
        sorted_sizes = sorted(size_names, key=lambda x: float(x) if x.replace('.', '', 1).isdigit() else x)
        sizes_str = ','.join(sorted_sizes)
        
        sorted_soles = sorted(sole_names)
        soles_str = ','.join(sorted_soles)

        
        # print("sole name list: ", sole_names)
        product_list.append({
            'id': shoe.id,
            'name': shoe.name,
            'brand': shoe.brand.name,
            'color': shoe.color.name,
            'price': float(shoe.price),
            'price_format': f"{shoe.price:,.0f}",
            'image_url': image_url,
            'sizes': sizes_str,
            'soles': soles_str
            # 'soles': soles_str
        })

    # Lấy danh sách brand để lọc
    brands = Brand.objects.all()

    # Lấy tất cả size (dùng cho bộ lọc)
    all_sizes = Size.objects.all()

    # Lấy danh sách loại đế duy nhất (nếu cần cho filter)
    sole_types = SoleType.objects.all()

    context = {
        'products': product_list,
        'brands': brands,
        'sizes': all_sizes,
        'soleTypes': sole_types,
    }
    return render(request, 'base.html', context)


# def product_detail(request, product_id):
#     shoe = get_object_or_404(Shoe.objects.prefetch_related('images', 'sizes'), pk=product_id)
#     images = shoe.images.all()
#     sizes = shoe.sizes.all().order_by('size')  # Sắp xếp size tăng dần
#     context = {
#         'shoe': shoe,
#         'images': images,
#         'sizes': sizes,
#     }
#     return render(request, 'product_detail.html', context)

# def product_detail(request, product_id):
#     # Lấy giày kèm ảnh và variants (kèm size và soleType)
#     shoe = get_object_or_404(
#         Shoe.objects.prefetch_related(
#             'images',
#             'variants__size',
#             'variants__soleType'
#         ).select_related('brand', 'color'),
#         pk=product_id
#     )
    
#     images = shoe.images.all()
    
#     # Tạo danh sách size duy nhất dưới dạng các dict giống cấu trúc ShoeSize cũ
#     # Mỗi dict có key 'size' (tên size) - template thường dùng {{ size.size }}
#     unique_size_names = shoe.variants.values_list('size__name', flat=True).distinct().order_by('size__name')
#     sizes = [{'size': name} for name in unique_size_names]  # giả lập object có thuộc tính 'size'
    
#     context = {
#         'shoe': shoe,
#         'images': images,
#         'sizes': sizes,
#     }
    
#     print(unique_size_names)
#     return render(request, 'product_detail.html', context)


def product_detail(request, product_id):
    # Lấy giày kèm ảnh và variants (kèm size và soleType)
    shoe = get_object_or_404(
        Shoe.objects.prefetch_related(
            'images',
            'variants__size',
            'variants__soleType'
        ).select_related('brand', 'color'),
        pk=product_id
    )
    
    images = shoe.images.all()
    # Lấy tất cả variants của giày, kèm thông tin size và soleType
    variants = shoe.variants.select_related('size', 'soleType').all()
    
    context = {
        'shoe': shoe,
        'images': images,
        'variants': variants,
        'price_format': f"{shoe.price:,.0f}",
    }
    
    return render(request, 'product_detail.html', context)