from django.db import models
from django.contrib.auth.models import User

# Create your models here.
STATE_CHOICES = (
    ('Bujumbura Mairie', 'Bujumbura Mairie'),
    ('Ruyigi', 'Ruyigi'),
    ('Ngozi', 'Ngozi'),
    ('Kirundo', 'Kirundo'),
    ('Gitega', 'Gitega'),
    ('Karuzi', 'Karuzi'),
    ('Rutana', 'Rutana'),
    ('Bujumbura Rural', 'Bujumbura Rural'),
    ('Muleba', 'Muleba'),
    ('Muleba', 'Muleba'),
    ('Muleba', 'Muleba'),
    ('Nairobi', 'Nairobi'),
    ('Mombasa', 'Mombasa'),
    ('Kisumu', 'Kisumu'),
    ('Nakuru', 'Nakuru'),
    ('Eldoret', 'Eldoret'),
    ('Thika', 'Thika'),
    ('Malindi', 'Malindi'),
    ('Kitale', 'Kitale'),
    ('Garissa', 'Garissa'),
)


CATEGORY_CHOICES = (
    ('CR', 'Curd'),
    ('ML', 'Milk'),
    ('LS', 'Lassi'),
    ('MS', 'Milkshake'),
    ('PN', 'Paneer'),
    ('GH', 'Ghee'),
    ('CZ', 'Cheese'),
    ('IC', 'Ice-cream'),
)
class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    composition = models.TextField(default='')
    prodapp = models.CharField(default='', max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to='product')

    def __str__(self):
        return self.title
    

#customer table
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    mobile = models.IntegerField(default=0)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=200)
    
    def __str__(self):
        return str(self.id)
    
#cart table
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

    class Meta:
        unique_together = ('user', 'product')

#order table
STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled'),
    ('pending', 'pending'),
)

class MpesaTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey('OrderPlaced', on_delete=models.CASCADE, related_name='mpesa_transactions')
    mpesa_transaction_id = models.CharField(max_length=255, unique=True)
    amount = models.FloatField()  # Amount paid in cents
    payment_status = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    payment = models.ForeignKey(MpesaTransaction, on_delete=models.CASCADE, null=True, blank=True)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=[('Mpesa', 'M-Pesa'), ('Other', 'Other')], default='Mpesa')

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.id)