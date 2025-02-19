"""
URL configuration for vegefoods project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from product_apps import views


urlpatterns = [
    path('product_management/',views.product_list, name='product_management'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),    
    path('product_view/',views.user_products, name='user_products'),
    path('product_details/<int:product_id>/',views.product_details, name='product_details'),
    path('toggle-product-listing/<int:product_id>/', views.toggle_product_listing, name='toggle_product_listing'),
    
    
]