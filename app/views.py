from django.shortcuts import render, redirect
from django.views import View
from . models import Product, Customer
from django.db.models import Count
from . forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages

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
            messages.success(request, 'User Registered Successfully')
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