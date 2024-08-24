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
from django.urls import path
from AdminAuth import views


urlpatterns = [
    path('login/', views.admin_login, name='admin_login'),
    path('panel/', views.panel, name='panel'),
    path('user_management/',views.user_managment, name='user_management'),
    path('user/<int:user_id>/block-unblock/',views.block_unblock_user,name='block_unblock_user'),
    path('logout',views.logout,name='logout')
    ]
