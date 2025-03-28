from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product

def homepage(request):
    return render(request, 'main/homepage.html')

class ProductList(ListView):
    model = Product
    template_name = 'main/ProductList.html'  # Opraveno na správnou cestu
    context_object_name = 'products'

class ProductDetail(DetailView):
    model = Product
    template_name = 'main/ProductDetail.html'  # Opraveno na správnou cestu
    context_object_name = 'product'
