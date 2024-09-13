from django.urls import path
from order_app import views


urlpatterns = [
    path('order/',views.place_order, name='place_order'),
    path('order-success/',views.order_success, name='order_success'),
    path('order-list/',views.user_order_list, name='order_list'),
    path('order-managment/',views.admin_order_list, name='order-managment'),
    path('order-view/<int:order_id>/', views.admin_order_details, name='order-view'),
    path('edit_address_checkout/<int:address_id>/', views.edit_checkout_address, name='edit_checkout_address'),
    path('add_addresses_checkout/', views.add_address_checkout, name='add_address_checkout'),
    path('order_details/<int:order_id>/', views.user_order_details, name='order_details'),
    path('checkout/order/<int:order_id>/update-status/', views.update_order_status, name='update_order_status'),
    path('download_invoice_item/<int:item_id>/', views.download_invoice_item, name='download_invoice_item'),
    path('razorpay/payment/status/', views.razorpay_payment_status, name='razorpay_payment_status'),
    path('cancel-order-item/<int:order_item_id>', views.user_cancel_order_item, name='user_cancel_order_item'),
    path('return-order-request/<int:order_item_id>', views.user_return_order_item, name='user_return_order_item'),

    ]