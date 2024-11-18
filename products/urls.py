from django.urls import path

# From current directory, import views.py
from . import views

# One empty path to indicate route URL which will render views.index with the name of home
urlpatterns = [
    path("", views.all_products, name="products"),
    path("<product_id>", views.product_detail, name="product_detail"),
]
