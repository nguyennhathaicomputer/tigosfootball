from django.db import models

# Create your models here.
class Brand(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class SoleType(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='sole_types', null=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = ('name', 'brand')

    def __str__(self):
        return self.name
    
class Color(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Shoe(models.Model):
    name = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='shoes')
    sole_type = models.ForeignKey(SoleType, on_delete=models.PROTECT, related_name='shoes')
    color = models.ForeignKey(Color, on_delete=models.PROTECT, related_name='shoes')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class ShoeSize(models.Model):
    shoe = models.ForeignKey(Shoe, on_delete=models.CASCADE, related_name='sizes')
    size = models.CharField(max_length=10)
    stock = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('shoe', 'size')

    def __str__(self):
        return f"{self.shoe.name} - Size {self.size}"
    


class ShoeImage(models.Model):
    shoe = models.ForeignKey(Shoe, on_delete=models.CASCADE, related_name='images')
    # Lưu URL từ Firebase
    image_url = models.ImageField(upload_to='shoes/') 
    # Tên file trên Firebase để dễ quản lý/xóa sau này
    # firebase_path = models.CharField(max_length=255, blank=True)
    
    # is_primary = models.BooleanField(default=False) # Ảnh đại diện chính
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"Image for {self.shoe.name}"

