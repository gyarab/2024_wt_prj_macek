from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product, Category
<<<<<<< HEAD
=======

def homepage(request):
    return render(request, 'main/homepage.html')
>>>>>>> d957692a50c771ae204977643fb9c2f5062e7db8

class ProductList(ListView):
    model = Product
    template_name = 'main/ProductList.html'
    context_object_name = 'products'

    def get_queryset(self):
<<<<<<< HEAD
        category_id = self.request.GET.get('category')
        subcategory_id = self.request.GET.get('subcategory')
        
        # Pokud je podkategorie, filtruj produkty podle ní
        if subcategory_id:
            return Product.objects.filter(category_id=subcategory_id)
        
        # Pokud je hlavní kategorie, filtruj podle ní
        if category_id:
            return Product.objects.filter(category__parent_id=category_id)
        
        return Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['main_categories'] = Category.objects.filter(parent__isnull=True)  # Hlavní kategorie
        context['selected_category'] = self.request.GET.get('category')
        context['selected_subcategory'] = self.request.GET.get('subcategory')
        
        # Pro každou hlavní kategorii načteme její podkategorie
        if context['selected_category']:
            context['subcategories'] = Category.objects.filter(parent_id=context['selected_category'])
        
=======
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
>>>>>>> d957692a50c771ae204977643fb9c2f5062e7db8
        return context

class ProductDetail(DetailView):
    model = Product
    template_name = 'main/ProductDetail.html'
    context_object_name = 'product'
