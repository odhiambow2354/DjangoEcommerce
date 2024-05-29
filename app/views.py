from django.shortcuts import render, redirect
from django.db.utils import IntegrityError
from django.http import JsonResponse
from django.views import View
from . models import Product, Customer, Cart, OrderPlaced, MpesaTransaction
from django.db.models import Count, Q
from . forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from DjangoEcommerce.settings import EMAIL_HOST_USER
from .models import Cart, OrderPlaced, MpesaTransaction, Wishlist
from .mpesa_handler import MpesaHandler


# Create your views here.
def home(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    
    return render(request, 'app/home.html', locals())

def about(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/about.html', locals())

def contact(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/contact.html', locals())


class CategoryView(View):
    def get(self, request, val):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
    
        # You can process the `val` here if needed
        
        product = Product.objects.filter(category=val)
        title= Product.objects.filter(category=val).values('title')
        return render(request, 'app/category.html', locals())
class CategoryTitle(View):
    def get(self, request, val):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
    
        # You can process the `val` here if needed
        
        product = Product.objects.filter(title=val)
        title= Product.objects.filter(category=product[0].category).values('title')
        return render(request, 'app/category.html', locals())
class ProductDetail(View):
    def get(self, request, pk):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        product = Product.objects.get(pk=pk)
        wishitem = Wishlist.objects.filter(product=product, user=request.user)
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
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
    
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
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    
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
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0.0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
        totalamount = amount + 30
    return render(request, 'app/addtocart.html', locals())
# Mpesa payment integration
class CheckoutView(View):

    def get(self, request):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = 0.0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount + value
        totalamount = famount + 30

        phone_number_form = CustomerProfileForm()

        context = {
            'user': user,
            'add': add,
            'cart_items': cart_items,
            'famount': famount,
            'totalamount': totalamount,
            'phone_number_form': phone_number_form,
        }

        return render(request, 'app/checkout.html', context)

    def post(self, request):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        user = request.user
        cart_items = Cart.objects.filter(user=user)
        famount = 0.0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount + value
        totalamount = famount + 30

        phone_number = request.POST.get('phone_number')
        phone_number_form = CustomerProfileForm(request.POST or None)  # Pass form data for validation

        # Address validation (optional)
        # ... add validation logic for phone number here

        context = {
            'user': user,
            'add': Customer.objects.filter(user=user),  # Refresh addresses
            'cart_items': cart_items,
            'famount': famount,
            'totalamount': totalamount,
            'phone_number_form': phone_number_form,
        }

        if phone_number_form.is_valid():  # Validate phone number form

            try:
                # Create MpesaHandler instance
                mpesa_handler = MpesaHandler()

                # Prepare payment data
                payment_data = {
                    'amount': totalamount,
                    'phone_number': phone_number,
                }

                # Initiate STK Push using MpesaHandler
                stk_push_response = mpesa_handler.make_stk_push(payment_data)

                if stk_push_response.get('ResponseCode') == '0':
                    # STK Push successful
                    checkout_request_id = stk_push_response.get('CheckoutRequestID')
                    mpesa_transaction = MpesaTransaction.objects.create(
                        user=user,
                        amount=totalamount,
                        phone_number=phone_number,
                        checkout_request_id=checkout_request_id,
                    )
                    # ... redirect to success page with relevant information

                else:
                    error_message = stk_push_response.get('ResponseMessage')
                    context['error_message'] = f"STK Push Failed: {error_message}"

            except Exception as e:
                context['error_message'] = f"An error occurred: {str(e)}"
        return render(request, 'app/checkout.html', locals())  # Or redirect to appropriate page



def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
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
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    
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
        amount = 0
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
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount += value
            totalamount = amount + 30
        data = {
            'amount': amount,
            'totalamount': totalamount 
        } 
        return JsonResponse(data)
    

def orders(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    
    order_placed = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', locals())

def plus_wishlist(request):
    wishitem = 0
    if request.user.is_authenticated:
        wishitem = len(Wishlist.objects.filter(user=request.user))
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist(user=user, product=product).save()
        data = {
            'message': 'Added to Wishlist'
        }
        return JsonResponse(data)
    
def minus_wishlist(request):
    wishitem = 0
    if request.user.is_authenticated:
        wishitem = len(Wishlist.objects.filter(user=request.user))
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist.objects.filter(Q(product=product) & Q(user=user)).delete()
        data = {
            'message': 'Removed from Wishlist'
        }
        return JsonResponse(data)
    
def search(request):
    query = request.GET['search']
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    product = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    return render(request, 'app/search.html', locals())