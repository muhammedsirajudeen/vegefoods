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
from django.contrib import admin
from django.urls import path, include
from UserAuth import views

urlpatterns = [
    path('adminn/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('admin/', include('AdminAuth.urls')),
    path('user/', include('UserAuth.urls')),
    path('categories/', include('category_app.urls')),
    path('products/', include('product_apps.urls')),
    path('profile/',include('profile_app.urls')),
    path('address/',include('address_app.urls')),
    path('cart/',include('cart_app.urls')),
    path('checkout/',include('order_app.urls')),
    path('wishlist/',include('wishlist_app.urls')),
    path('coupon/',include('coupen_app.urls')),
    path('wallet/',include('wallet.urls')),
    path('', views.redirect_to_home), 
]

handler404 = "UserAuth.views.handle_not_found"