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
from UserAuth import views
from .views import CustomPasswordResetView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('home/', views.user_home, name='home'),
    path('signup/', views.user_registration, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('verify-otp/<int:user_id>/', views.verify_otp, name='verify_otp'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),
    
    path('password_reset/', CustomPasswordResetView.as_view(template_name='user/password_reset_form.html'), name='password_reset'),    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'), name='password_reset_complete'),
    path('count-cart/', views.count_cart, name='count_cart'),  # Add this line
    path('about/', views.About_page, name='about'),  # Add this line
    path('contact/', views.Contact_page, name='contact'),  # Add this line
    path('api/wallet-balance/', views.get_wallet_balance, name='wallet_balance'),
    path('api/recipe-suggestions/', views.recipe_suggestions, name='recipe_suggestions'),

]
