from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product, Category

def homepage(request):
    return render(request, 'main/homepage.html')

class ProductList(ListView):
    model = Product
    template_name = 'main/ProductList.html'
    context_object_name = 'products'

    def get_queryset(self):
        """
        Filtrování produktů podle kategorie.
        """
        category_id = self.kwargs.get('category_id')
        if category_id:
            return Product.objects.filter(category__id=category_id)
        return Product.objects.all()

    def get_context_data(self, **kwargs):
        """
        Přidání kategorie do kontextu pro šablonu.
        """
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        if category_id:
            context['category'] = Category.objects.get(id=category_id)
        return context

class ProductDetail(DetailView):
    model = Product
    template_name = 'main/ProductDetail.html'
    context_object_name = 'product'
