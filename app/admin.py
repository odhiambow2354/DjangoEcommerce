from django.contrib import admin
from .models import Product

# Register your models here.
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'selling_price', 'discounted_price', 'category', 'description',  'product_image']
    list_filter = ['category']
    search_fields = ['title', 'category']
    list_per_page = 6
