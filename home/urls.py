from django.contrib import admin
from django.urls import path

# From current directory, import views.py
from . import views

# One empty path to indicate route URL which will render views.index with the name of home
urlpatterns = [path("", views.index, name="home")]
