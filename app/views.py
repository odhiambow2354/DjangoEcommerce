from django.shortcuts import render, redirect
from django.db.utils import IntegrityError
from django.http import JsonResponse
from django.views import View
from . models import Product, Customer, Cart
from django.db.models import Count, Q
from . forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from DjangoEcommerce.settings import EMAIL_HOST_USER

# Create your views here.
def home(request):
    return render(request, 'app/home.html')

def about(request):
    return render(request, 'app/about.html')

def contact(request):
    return render(request, 'app/contact.html')


class CategoryView(View):
    def get(self, request, val):
        # You can process the `val` here if needed
        
        product = Product.objects.filter(category=val)
        title= Product.objects.filter(category=val).values('title')
        return render(request, 'app/category.html', locals())
class CategoryTitle(View):
    def get(self, request, val):
        # You can process the `val` here if needed
        
        product = Product.objects.filter(title=val)
        title= Product.objects.filter(category=product[0].category).values('title')
        return render(request, 'app/category.html', locals())
class ProductDetail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, 'app/product_detail.html', locals())
    
class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customer_registration.html', locals())
    
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User Registered Successfully, Login')
        else:
            messages.warning(request, "Invalid inputs, please try again")
        return render(request, 'app/customer_registration.html', locals())
    
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', locals())
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(user=user, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Profile Updated Successfully')
        else:
            messages.warning(request, "Invalid inputs, please try again")
        return render(request, 'app/profile.html', locals())
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', locals())

class updateAddress(View):
    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request, 'app/update_address.html', locals())
    
    def post(self, request, pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.mobile = form.cleaned_data['mobile']
            add.save()
            messages.success(request, 'Profile Updated Successfully')
        else:
            messages.warning(request, "Invalid inputs, please try again")
        return redirect('address')

#send email
def sendmail(request):
    subject = 'Welcome to Django Ecommerce!'
    message = f'Hello {request.user.username},\n\nWelcome aboard! We are thrilled to have you as part of our community at Django Ecommerce. Our mission is to provide you with an exceptional shopping experience, offering a wide range of products and top-notch customer service.\n\nWe hope you enjoy exploring our website and discovering our latest offerings. Should you have any questions or need assistance, feel free to reach out to us anytime.\n\nThank you for choosing Django Ecommerce. Happy shopping!\n\nBest regards,\nThe Django Ecommerce Team'
    recipient = str(request.user.email)
    send_mail(subject, message, EMAIL_HOST_USER, [recipient], fail_silently=False)
    return render(request, 'app/success.html', {'recipient': recipient})



#add to cart
def add_to_cart(request):
    if request.method == 'GET':
        user = request.user
        product_id = request.GET.get('prod_id')
        product = Product.objects.get(id=product_id)
        try:
            # Attempt to add the product to the cart
            Cart.objects.create(user=user, product=product)
            return redirect('/cart')
        except IntegrityError:
            # Handle the case where the product is already in the cart
            return redirect(f'/product-detail/{product_id}')
        
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0.0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
        totalamount = amount + 30
    return render(request, 'app/addtocart.html', locals())

class checkout(View):
    def get(self, request):
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = 0.0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount + value
        totalamount = famount + 30
        return render(request, 'app/checkout.html', locals())

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
            totalamount = amount + 30
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        } 
        return JsonResponse(data)
    
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))

        if c.quantity > 1:
            c.quantity -= 1
            c.save()
        else:
            c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount += value
            totalamount = amount + 30
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount 
        } 
        return JsonResponse(data)
    
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount += value
            totalamount = amount + 30
        data = {
            'amount': amount,
            'totalamount': totalamount 
        } 
        return JsonResponse(data)
    