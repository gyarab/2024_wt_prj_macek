from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from main import views
from django.views.generic import TemplateView
from django.conf import settings 
from django.conf.urls.static import static 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='main/homepage.html'), name='homepage'),
<<<<<<< HEAD
    path('products/', views.ProductList.as_view(), name='product_list'),
    path('products/category/<int:category_id>/', views.ProductList.as_view(), name='category_products'),
=======
    path('products/', views.ProductList.as_view(), name='product_list'),  # Zobrazení všech produktů
    path('category/<int:category_id>/', views.ProductList.as_view(), name='product_list_by_category'),  # Zobrazení produktů podle kategorie
>>>>>>> d957692a50c771ae204977643fb9c2f5062e7db8
    path('product/<int:pk>/', views.ProductDetail.as_view(), name='product_detail'),
]

if settings.DEBUG:
<<<<<<< HEAD
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
=======
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
>>>>>>> d957692a50c771ae204977643fb9c2f5062e7db8
