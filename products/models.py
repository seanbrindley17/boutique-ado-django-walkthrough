from django.db import models


# Create your models here.
# Category inherits from models.Model
class Category(models.Model):
    # name is more programmatic for seatching
    name = models.CharField(max_length=254)
    # null & blank being true makes it optional. nicer display name
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        # Adjusts name field from default model name to category name
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


# Each Product requires name, description and price. Everything else is optional
class Product(models.Model):
    # Foreign key to category model which is null in db and blank in forms
    # If category is deleted, change category to SET_NULL instead of deleting product
    category = models.ForeignKey(
        "Category", null=True, blank=True, on_delete=models.SET_NULL
    )
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        # Adjusts name field from default model name to category name
        return self.name
