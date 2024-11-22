# For financial transactions, Decimal is preferred to Float as Float has a tendency for rounding errors
from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404

# From models.py in products directory, import Product class
from products.models import Product


# This is a context processor. its purpose is to make this dictionary available to all templates across the entire application
# These are added to [project level directory]/settings.py within Templates -> OPTIONS -> context_processors
def bag_contents(request):

    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get("bag", {})

    # For each item ID and quantity (item_data) in the bag from the session
    for item_id, item_data in bag.items():
        # Check if the item data is just an integer, if so then it will just be quantity added and not size
        if isinstance(item_data, int):
            # Get the product using get_object, primary key is it's item id
            product = get_object_or_404(Product, pk=item_id)
            # Product multiplied by quantity bought is added to total
            total += item_data * product.price
            # Increments product_count by the quantity
            product_count += item_data
            # Add to the bag_items dictionary the ID and quantity of item and also the product object itself
            bag_items.append(
                {"item_id": item_id, "quantity": item_data, "product": product}
            )
        # If there are item sizes in the data being added
        else:
            product = get_object_or_404(Product, pk=item_id)
            # Iterate through the inner dictionary of "items_by_size"
            for size, quantity in item_data["items_by_size"].items():
                # Increment total and product count accordingly
                total += quantity * product.price
                product_count += quantity
                # Add "size" to the bag_items dictionary
                bag_items.append(
                    {
                        "item_id": item_id,
                        "quantity": quantity,
                        "product": product,
                        "size": size,
                    }
                )

    # Check if the bag items total cost is less than the free delivery threshold
    if total < settings.FREE_DELIVERY_THRESHOLD:
        # If so, calculate the delivery cost as total multiplied by the standard delivery percentage specified in settings
        # Wrapped in Decimal function as it's a financial transaction
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE)
        # Will tell the user how much more they need to spend to qualify for free delivery
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        # Otherwise, delivery cost is 0 and therefore the free delivery delta above is 0 too
        delivery = 0
        free_delivery_delta = 0

    # Simply the total cost of the bag items plus the delivery cost
    grand_total = delivery + total

    # Adding all these items to the context to make them available across the site
    context = {
        "bag_items": bag_items,
        "total": total,
        "product_count": product_count,
        "delivery": delivery,
        "free_delivery_delta": free_delivery_delta,
        "free_delivery_threshold": settings.FREE_DELIVERY_THRESHOLD,
        "grand_total": grand_total,
    }

    return context
