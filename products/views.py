from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages

# Q is a query sorting helper, explanation in Queries and Categories part 1
from django.db.models import Q

# from products/models.py import Product class
from .models import Product

# Create your views here.


# View to show all products, sorting and search queries
def all_products(request):

    # Returns all products from the Product database
    products = Product.objects.all()
    # Should allow products page to initially load without throwing an error for having no search term
    query = None

    if request.GET:
        # "q" corresponds to the name field in the search input
        if "q" in request.GET:
            # sets the search value from "q" to variable called query
            query = request.GET["q"]
            # If query is blank
            if not query:
                # Flash message
                messages.error(request, "No search criteria entered")
                # Redirect to products url
                return redirect(reverse("products"))
            # Sets queries to a Q object where name or description contains the query entered
            # The | between them generates the "or", and "i" before contains makes the query case insensitive
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            # Filter the products by the query seached for
            products = products.filter(queries)

    # Allows products to be available in template. Like doing products=products in a Flask function in the render_template
    context = {
        "products": products,
        "search_term": query,
    }

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
