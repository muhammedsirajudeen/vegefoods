from django.urls import path
from . import views

urlpatterns = [
    path('coupon_management/', views.admin_coupon_management,name='coupon_management'),  #
    path('delete_coupon/<int:coupon_id>/', views.delete_coupon, name='delete_coupon'),  
    path('edit_coupen<int:coupon_id>/',views.edit_coupon,name='edit_coupon')
]