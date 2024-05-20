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