from django.shortcuts import render

# from products/models.py import Product class
from .models import Product

# Create your views here.


# View to show all products, sorting and search queries
def all_products(request):

    # Returns all products from the Product database
    products = Product.objects.all()

    # Allows products to be available in template. Like doing products=products in a Flask function in the render_template
    context = {"products": products}

    # Returns products.html, needs context as some things will be send back to template
    return render(request, "products/products.html", context)
