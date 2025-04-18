from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, TemplateView
from .models import Product, Category, Cart, CartItem
from django.contrib.auth.models import User

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

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Pokud je uživatel přihlášen, použij jeho uživatelský košík, jinak použij session
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
        cart, created = Cart.objects.get_or_create(session_key=session_key)

    # Přidej nebo aktualizuj položku v košíku
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()  # Nezapomeň uložit změny!

    return JsonResponse({'cart_count': cart.get_item_count()})
