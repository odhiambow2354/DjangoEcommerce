from django.contrib import admin
from .models import Product, Customer, Cart, OrderPlaced, MpesaTransaction, Wishlist
from django.urls import reverse
from django.utils.html import format_html

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
    list_display = ['id', 'user', 'products', 'quantity']
    list_filter = ['user']
    search_fields = ['user']
    list_per_page = 6
    def products(self, obj):
        link = reverse('admin:app_product_change', args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.title)


@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customers', 'products', 'quantity', 'ordered_date', 'status',]
    def products(self, obj):
        link = reverse('admin:app_product_change', args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.title)
    
    def customers(self, obj):
        link = reverse('admin:app_customer_change', args=[obj.customer.pk])
        return format_html('<a href="{}">{}</a>', link, obj.customer.name)
    
    list_filter = ['status']
    search_fields = ['user', 'customer']
    list_per_page = 6

@admin.register(MpesaTransaction)
class MpesaTransactionModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'order', 'mpesa_transaction_id', 'amount', 'payment_status', 'timestamp']
    list_filter = ['payment_status']
    search_fields = ['user', 'order']
    list_per_page = 6

@admin.register(Wishlist)
class WishlistModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'products']
    def products(self, obj):
        link = reverse('admin:app_product_change', args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.title)

    list_filter = ['user']
    search_fields = ['user']
    list_per_page = 6