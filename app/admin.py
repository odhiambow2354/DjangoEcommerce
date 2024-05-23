from django.contrib import admin
from .models import Product, Customer, Cart

# Register your models here.
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'selling_price', 'discounted_price', 'category', 'description',  'product_image']
    list_filter = ['category']
    search_fields = ['title', 'category']
    list_per_page = 6

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'locality', 'city', 'zipcode']
    list_filter = ['city']
    search_fields = ['name', 'city']
    list_per_page = 6

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']
    list_filter = ['user']
    search_fields = ['user']
    list_per_page = 6