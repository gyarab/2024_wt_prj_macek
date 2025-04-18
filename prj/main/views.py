from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from .models import Product, Category

class ProductList(ListView):
    model = Product
    template_name = 'main/ProductList.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_id = self.request.GET.get('category')
        subcategory_id = self.request.GET.get('subcategory')

        if subcategory_id:
            return Product.objects.filter(category_id=subcategory_id)

        if category_id:
            return Product.objects.filter(category__parent_id=category_id)

        return Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['main_categories'] = Category.objects.filter(parent__isnull=True)
        context['selected_category'] = self.request.GET.get('category')
        context['selected_subcategory'] = self.request.GET.get('subcategory')

        if context['selected_category']:
            context['subcategories'] = Category.objects.filter(parent_id=context['selected_category'])

        return context

class ProductDetail(DetailView):
    model = Product
    template_name = 'main/ProductDetail.html'
    context_object_name = 'product'

class CartView(TemplateView):
    template_name = 'main/Cart.html'
