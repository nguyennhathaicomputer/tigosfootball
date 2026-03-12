from django.shortcuts import render
from .models import Shoe, Brand, ShoeSize

# Create your views here.
def home(request):
    # Lấy tất cả giày, kèm ảnh đầu tiên, giá, màu, brand
    if not request.user.is_authenticated:
    
        shoes = Shoe.objects.prefetch_related('images', 'sizes').select_related('brand', 'color').all()
        
        # Chuẩn bị dữ liệu để truyền vào template
        product_list = []
        for shoe in shoes:
            first_image = shoe.images.first()
            image_url = first_image.image_url.url if first_image else '/static/images/default.jpg'
            # Lấy danh sách size của sản phẩm (dạng chuỗi để gán vào data-attribute)
            sizes = shoe.sizes.values_list('size', flat=True)
            sizes_str = ','.join([str(s) for s in sizes])
            
            product_list.append({
                'id': shoe.id,
                'name': shoe.name,
                'brand': shoe.brand.name,
                'color': shoe.color.name,
                'price': float(shoe.price),
                'image_url': image_url,
                'sizes': sizes_str,
            })
        
        # Lấy tất cả brand để hiển thị checkbox filter (nếu sidebar cần dynamic)
        brands = Brand.objects.all()
        # Có thể lấy tất cả size duy nhất từ tất cả giày (nếu cần)
        all_sizes = ShoeSize.objects.values_list('size', flat=True).distinct().order_by('size')
        
        context = {
            'products': product_list,
            'brands': brands,
            'sizes': all_sizes,
        }
    return render(request, 'base.html', context)


