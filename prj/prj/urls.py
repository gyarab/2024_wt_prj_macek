from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='main/homepage.html'), name='homepage'), 
    path('one/', TemplateView.as_view(template_name='main/one.html'), name='one'),
    path('two/', TemplateView.as_view(template_name='main/two.html'), name='two'),
]
