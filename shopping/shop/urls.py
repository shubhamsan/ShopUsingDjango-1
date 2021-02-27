from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('cart/', views.cart, name='cart'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('checkout/', views.checkout, name='checkout'),
    path('productview/<int:myid>', views.productview, name='productview'),
    path('callback/', views.callback, name='callback'),
    path('canceled/', views.canceled, name='canceled'),



    
]