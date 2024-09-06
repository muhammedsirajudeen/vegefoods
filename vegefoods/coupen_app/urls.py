from django.urls import path
from . import views

urlpatterns = [
    path('coupen_management/', views.admin_coupen_mangement, name='coupen_management'),  #

]