from django.contrib import admin
from .models import Category, Product, Address, Order, OrderItem

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'available')
    list_filter = ('category', 'available')
    search_fields = ('name', 'description')

class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'street', 'city', 'zip_code')
    list_filter = ('user', 'city')
    search_fields = ('street', 'city', 'zip_code')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'total_price', 'status')
    list_filter = ('user', 'status')
    search_fields = ('user__username',) 

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    list_filter = ('order',)
    search_fields = ('product__name',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)