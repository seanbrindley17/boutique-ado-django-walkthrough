from django.contrib import admin

# From models.py in same directory import the Product model
from .models import Product, Category

# Register your models here.


# Extends from built in Django ModelAdmin class
class ProductAdmin(admin.ModelAdmin):
    # Tells the admin what to display. Use this to adjust display order if needed
    list_display = (
        "sku",
        "name",
        "category",
        "price",
        "rating",
        "image",
    )

    # Sorts by sku. Has to be a tuple so need the comma
    # To reverse sort, add minus sign before i.e. -"sku"
    ordering = ("sku",)


class CategoryAdmin(admin.ModelAdmin):
    # Makes sure these category names are displayed to admin here
    list_display = (
        "friendly_name",
        "name",
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
