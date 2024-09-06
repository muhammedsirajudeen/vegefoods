from django.urls import path
from . import views

urlpatterns = [
    path('cart_view/', views.cart_view, name='cart'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),  
    path('update-quantity/', views.update_quantity, name='update_quantity'),
    ]