# Description: This file is used to define the URL patterns for the app.
from . import views
from django.urls import path

urlpatterns = [
    path('', views.home),
]
