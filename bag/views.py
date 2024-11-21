from django.shortcuts import render, redirect


# Create your views here.


# View that renders the bag contents page
def view_bag(request):

    return render(request, "bag/bag.html")


# Add a specified quantity of a product to the bag
def add_to_bag(request, item_id):
    # Need to use int() method on the quantity input to convert to integer as it will be passed as a string
    quantity = int(request.POST.get("quantity"))
    # Gets the redirect_url from the hidden input so the site knows where to redirect the user
    redirect_url = request.POST.get("redirect_url")
    # Initially set size variable to none
    size = None
    # If product size exists in the form POSTed
    if "product_size" in request.POST:
        # Set size variable to size posted
        size = request.POST["product_size"]

    # Variable "bag" accesses requests.session to see if the session already exists, and opens an empty dictionary if not
    bag = request.session.get("bag", {})

    # If size exists in an item in the session
    if size:
        # If the item_id already exists in the bag's keys
        if item_id in list(bag.keys()):
            # Check if the size of the item being added also exists in the bag keys
            if size in bag[item_id]["items_by_size"].keys():
                # Increment the quantity by amount being added
                bag[item_id]["items_by_size"][size] += quantity
            # If the size of the item doesn't already exist in the bag keys
            else:
                # Set the quantity variable to the amount being added
                bag[item_id]["items_by_size"][size] = quantity
        else:
            # If the item isn't already in bag, add as dictionary with key: "items_by_size"
            # This allows items with the same item_id and different sizes to be separated and tracked by size
            bag[item_id] = {"items_by_size": {size: quantity}}
    else:
        # If there's already a key in the bag which matches the product ID being added
        if item_id in list(bag.keys()):
            # Increment the quantity by how ever many are being added
            bag[item_id] += quantity
        else:
            # Creates key with items's ID which is equal to the quantity
            bag[item_id] = quantity

    # Overwrites the bag variable in the session with the updated bag variable
    request.session["bag"] = bag
    print(request.session["bag"])
    # Redirects user to the redirect url from the hidden input in the form
    return redirect(redirect_url)
