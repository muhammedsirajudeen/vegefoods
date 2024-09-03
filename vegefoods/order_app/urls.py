from django.urls import path
from order_app import views


urlpatterns = [
    path('order/',views.place_order, name='place_order'),
    path('order-success/',views.order_success, name='order_success'),
    path('order-details/',views.user_order_details, name='order_details'),
    path('order-managment/',views.admin_order_list, name='order-managment'),
    path('order-view/<int:order_id>/', views.admin_order_details, name='order-view'),
]