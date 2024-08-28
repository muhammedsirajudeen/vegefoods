from django.urls import path
from . import views

urlpatterns = [
    path('cart_view/', views.cart_view, name='cart_view'), 
    path('add_to_cart/',views.add_to_cart,name='add_to_cart') #


]