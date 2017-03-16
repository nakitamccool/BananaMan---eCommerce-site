from django.shortcuts import render
from models import Product

# Create your views here

def index(request):
    return render(request, 'index.html')

def all_products(request):
    products = Product.objects.all()
    return render(request, "products.html", {"products": products})