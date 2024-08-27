from django.urls import path
from AdminAuth import views
from address_app import views

urlpatterns = [
    path('user_addresses/', views.user_address, name='user_address'),
    path('add_addresses/', views.add_address, name='add_address'),
    path('edit_address/<int:address_id>/', views.edit_address, name='edit_address'),
    ]
