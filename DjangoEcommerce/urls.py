# Description: This file is the main URL configuration for the DjangoEcommerce project. It includes the URL configuration for the app.
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
]
