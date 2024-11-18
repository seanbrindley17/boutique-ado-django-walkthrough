from django.contrib import admin

# From models.py in same directory import the Product model
from .models import Product, Category

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
