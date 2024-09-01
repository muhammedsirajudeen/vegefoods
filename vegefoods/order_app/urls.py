from django.urls import path
from order_app import views


urlpatterns = [
    path('order/',views.place_order, name='place_order'),
    path('order-success/',views.order_success, name='order_summary'),
    
]