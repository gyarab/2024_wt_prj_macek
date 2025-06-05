from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, TemplateView
from .models import Product, Category, Cart, CartItem
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json

def calculate_cart_total(cart_obj):
    total = sum(item.product.price * item.quantity for item in CartItem.objects.filter(cart=cart_obj))
    return total

def get_cart_item_count(cart_obj):
    count = sum(item.quantity for item in CartItem.objects.filter(cart=cart_obj))
    return count

def get_user_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart

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
        cart = get_user_cart(self.request)

        cart_items = CartItem.objects.filter(cart=cart)
        total_price = calculate_cart_total(cart)
        
        context['cart_items'] = cart_items
        context['total_price'] = total_price
        
        return context

@require_POST
def add_to_cart(request):
    data = json.loads(request.body)
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    product = get_object_or_404(Product, id=product_id)
    cart = get_user_cart(request)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += int(quantity)
    cart_item.save()

    cart_count = get_cart_item_count(cart)
    total_price = calculate_cart_total(cart)

    return JsonResponse({'success': True, 'cart_count': cart_count, 'total_price': total_price})

@require_POST
def update_cart_quantity(request):
    data = json.loads(request.body)
    product_id = data.get('product_id')
    action = data.get('action')

    cart = get_user_cart(request)

    try:
        item = CartItem.objects.get(cart=cart, product_id=product_id)
        
        new_quantity = item.quantity

        if action == 'increment':
            new_quantity += 1
        elif action == 'decrement':
            new_quantity -= 1
        
        if new_quantity <= 0:
            item.delete()
            new_quantity = 0 
        else:
            item.quantity = new_quantity
            item.save()

        current_total_price = calculate_cart_total(cart)
        current_cart_items_count = get_cart_item_count(cart)

        return JsonResponse({
            'success': True,
            'new_quantity': new_quantity,
            'total_price': current_total_price,
            'cart_count': current_cart_items_count
        })
    except CartItem.DoesNotExist:
        current_total_price = calculate_cart_total(cart)
        current_cart_items_count = get_cart_item_count(cart)
        return JsonResponse({
            'success': True,
            'new_quantity': 0,
            'total_price': current_total_price,
            'cart_count': current_cart_items_count,
            'message': 'Položka již není v košíku.'
        }, status=200)
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Chyba při aktualizaci množství: {e}'}, status=500)

@require_POST
@csrf_exempt
def remove_from_cart(request):
    data = json.loads(request.body)
    product_id = data.get('product_id')

    cart = get_user_cart(request)

    try:
        item_to_delete = CartItem.objects.get(cart=cart, product_id=product_id)
        item_to_delete.delete()
        
        current_total_price = calculate_cart_total(cart)
        current_cart_items_count = get_cart_item_count(cart)

        return JsonResponse({
            'success': True,
            'total_price': current_total_price,
            'cart_count': current_cart_items_count
        })
    except CartItem.DoesNotExist:
        current_total_price = calculate_cart_total(cart)
        current_cart_items_count = get_cart_item_count(cart)
        return JsonResponse({
            'success': True,
            'total_price': current_total_price,
            'cart_count': current_cart_items_count,
            'message': 'Položka již byla odstraněna z košíku.'
        }, status=200)
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Chyba při odstraňování: {e}'}, status=500)

class CheckoutView(TemplateView):
    template_name = 'main/checkout.html'