from django.shortcuts import render, get_object_or_404

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


# View to show individual product details
def product_detail(request, product_id):

    # Returns a product by it's project ID, or a 404 error if not found
    product = get_object_or_404(Product, pk=product_id)

    # Allows product above to be available in template.
    context = {"product": product}

    # Returns product_detail.html, needs context as some things will be send back to template
    return render(request, "products/product_detail.html", context)
