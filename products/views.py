from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.db.models.functions import Lower

# Q is a query sorting helper, explanation in Queries and Categories part 1
from django.db.models import Q

# from products/models.py import Product and Category class
from .models import Product, Category

# Create your views here.


# View to show all products, sorting and search queries
def all_products(request):

    # Returns all products from the Product database
    products = Product.objects.all()
    # Should allow products page to initially load without throwing an error for having no search term
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        # If a sort request by the user is chosen
        if "sort" in request.GET:
            # Gets the sort request and stores in "sortkey"
            sortkey = request.GET["sort"]
            # storing the sort in sortkey allows the original field the was sorted on to be preserved
            sort = sortkey
            # Check if sortkey is equal to "name"
            if sortkey == "name":
                # If so, store sortkey in new variable named lower_name if user is sorting by name
                sortkey = "lower_name"
                # using products.annotate adds temporary field to model to allow for case insensitive sorting in field name in this case
                products = products.annotate(lower_name=Lower("name"))
            # Check if the sortkey is a category
            if sortkey == "category":
                # Double underscore allows drilling into a related model
                # Essentially makes products = products.order_by(category__name)
                sortkey = "category__name"

            if "direction" in request.GET:
                # Checks direction in sort request
                direction = request.GET["direction"]
                # If it's descending
                if direction == "desc":
                    # Format the string using "f" and placing a minus sign before { } with the variable in to reverse it
                    sortkey = f"-{sortkey}"
            # Sorts the products based on the logic above using order_by()
            products = products.order_by(sortkey)

        # If a category is searched for
        if "category" in request.GET:
            # Split into a list of categories by comma, if applicable
            categories = request.GET["category"].split(",")
            # Filter products to show only products whose category name is in the list
            products = products.filter(category__name__in=categories)
            # Coverts the list of strings of category names passed through URL to their actual category object
            categories = Category.objects.filter(name__in=categories)
            # double underscore __ is best practice when making django query logic

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
    # Tells the template the current sorting logic using string formatting
    current_sorting = f"{sort}_{direction}"

    # Allows products to be available in template. Like doing products=products in a Flask function in the render_template
    context = {
        "products": products,
        "search_term": query,
        "current_categories": categories,
        "current_sorting": current_sorting,
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
