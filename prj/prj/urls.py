from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from main import views
from django.views.generic import TemplateView
from main.views import ProductList, ProductDetail, CartView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='main/homepage.html'), name='homepage'),
    path('products/', views.ProductList.as_view(), name='product_list'),
    path('products/category/<int:category_id>/', views.ProductList.as_view(), name='category_products'),
    path('product/<int:pk>/', views.ProductDetail.as_view(), name='product_detail'),
    path('cart/', CartView.as_view(), name='cart'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
