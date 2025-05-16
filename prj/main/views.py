from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, TemplateView
from .models import Product, Category, Cart, CartItem
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json

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
        selected_category_id = self.request.GET.get('category')
        selected_subcategory_id = self.request.GET.get('subcategory')

        context['main_categories'] = Category.objects.filter(parent__isnull=True)
        context['selected_category'] = selected_category_id
        context['selected_subcategory'] = selected_subcategory_id

        if selected_category_id:
            context['subcategories'] = Category.objects.filter(parent_id=selected_category_id)

            try:
                selected_category = Category.objects.get(id=selected_category_id)
                context['selected_category_name'] = selected_category.name
            except Category.DoesNotExist:
                context['selected_category_name'] = None
        else:
            context['selected_category_name'] = None

        return context

class ProductDetail(DetailView):
    model = Product
    template_name = 'main/ProductDetail.html'
    context_object_name = 'product'

class CartView(TemplateView):
    template_name = 'main/Cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Pokud je uživatel přihlášen, použij jeho košík, jinak session_key
        if self.request.user.is_authenticated:
            cart = Cart.objects.filter(user=self.request.user).first()
        else:
            session_key = self.request.session.session_key
            if not session_key:
                self.request.session.create()  # Vytvoří session_key, pokud ještě není
            cart = Cart.objects.filter(session_key=session_key).first()

        if cart:
            cart_items = CartItem.objects.filter(cart=cart)
            total_price = sum(item.product.price * item.quantity for item in cart_items)
            context['cart_items'] = cart_items
            context['total_price'] = total_price
        else:
            context['cart_items'] = []
            context['total_price'] = 0

        return context

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Pokud je uživatel přihlášen, použij jeho košík, jinak session_key
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()  
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return JsonResponse({'cart_count': cart.get_item_count()})

@require_POST
@csrf_exempt
def update_cart_quantity(request):
    data = json.loads(request.body)
    product_id = data.get('product_id')
    action = data.get('action')

    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            return JsonResponse({'error': 'Session not found'}, status=400)
        cart = Cart.objects.get(session_key=session_key)

    try:
        cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
        
        if action == 'increment':
            cart_item.quantity += 1
        elif action == 'decrement':
            cart_item.quantity = max(cart_item.quantity - 1, 1)  
        cart_item.save()

        return JsonResponse({'success': True, 'new_quantity': cart_item.quantity})
    
    except CartItem.DoesNotExist:
        return JsonResponse({'error': 'Item not found in cart'}, status=404)

@require_POST
@csrf_exempt
def remove_from_cart(request):
    data = json.loads(request.body)
    product_id = data.get('product_id')

    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            return JsonResponse({'error': 'Session not found'}, status=400)
        cart = Cart.objects.get(session_key=session_key)

    CartItem.objects.filter(cart=cart, product_id=product_id).delete()
    return JsonResponse({'success': True})

class CheckoutView(TemplateView):
    template_name = 'main/checkout.html'
