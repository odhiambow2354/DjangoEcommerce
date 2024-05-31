Project Name: Dairy Products Ecommerce

Description

This is a Django e-commerce project that allows users to browse products, add them to their cart and wishlist, and manage their transactions. The project leverages AJAX for dynamic updates and provides a user-friendly shopping experience.

Features

    Product Catalog: Browse a variety of products with details and images.
    Cart Management: Add and remove items from the cart with quantity adjustments.
    Wishlist Functionality: Add and remove items from a user's wishlist for later consideration.
    AJAX Integration: Update cart and wishlist counts dynamically without full page reloads.
    Payment Integration: In progress

Requirements
    Django 

Installation

    Clone this repository:
    git clone git@github.com:odhiambow2354/DjangoEcommerce.git

Create a virtual environment (recommended):

    python -m venv venv
    source venv/bin/activate  
# Windows: venv\Scripts\activate.bat

Install dependencies:

    pip install -r requirements.txt

Apply database migrations:
    python manage.py makemigrations
    python manage.py migrate

Create a superuser for administrative access:

    python manage.py createsuperuser

Run the development server:

    python manage.py runserver


Usage

    Access the application in your web browser at http://localhost:8000/ (or the port specified in your settings).
    Browse products, add them to your cart and wishlist using the provided buttons.
    Manage items in your cart and wishlist as needed.

Payment Integration : 
Create developer account and get the necessary credentials
Contributing

I welcome contributions to this project! Please feel free to fork the repository, make changes, and submit pull requests.