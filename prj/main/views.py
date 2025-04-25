from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, TemplateView
from .models import Product, Category, Cart, CartItem
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm

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

        if self.request.user.is_authenticated:
            cart = Cart.objects.filter(user=self.request.user).first()
        else:
            session_key = self.request.session.session_key
            if not session_key:
                self.request.session.create()  
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
    if request.user.is_authenticated:
        product = Product.objects.get(id=product_id)

        cart = request.session.get('cart', {})
        if product_id in cart:
            cart[product_id] += 1  
        else:
            cart[product_id] = 1  
        request.session['cart'] = cart

        cart_item_count = sum(cart.values())
        return JsonResponse({'cart_count': cart_item_count})

    return redirect('login')  

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
def remove_from_cart(request, product_id):
    data = json.loads(request.body)
    product_id = data.get('product_id')

    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            return JsonResponse({'error': 'Session not found'}, status=400)
        cart = Cart.objects.get(session_key=session_key)

    # Zkontrolujeme, zda je položka v košíku
    cart_item = CartItem.objects.filter(cart=cart, product_id=product_id).first()
    if not cart_item:
        return JsonResponse({'error': 'Product not found in cart'}, status=400)

    cart_item.delete()
    return JsonResponse({'success': True})


class CheckoutView(TemplateView):
    template_name = 'main/checkout.html'

def login_view(request):
    return render(request, 'main/login.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('homepage')
    else:
        form = AuthenticationForm()

    return render(request, 'main/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']

        if password != password_confirm:
            return render(request, 'main/register.html', {'error': 'Hesla se neshodují.'})
        
        if User.objects.filter(username=username).exists():
            return render(request, 'main/register.html', {'error': 'Uživatelské jméno je již zaregistrováno.'})

        user = User.objects.create_user(username=username, password=password)

        login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        return redirect('homepage')  

    return render(request, 'main/register.html')
