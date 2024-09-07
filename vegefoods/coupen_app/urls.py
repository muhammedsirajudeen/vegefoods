from django.urls import path
from . import views

urlpatterns = [
    path('coupon_management/', views.admin_coupon_management,name='coupon_management'),  #

]