from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('one/', views.one, name='one'),
    path('two/', views.two, name='two'),
]
