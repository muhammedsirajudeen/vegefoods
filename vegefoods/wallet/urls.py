from django.urls import path
from . import views

urlpatterns = [
    path('<int:user_id>/', views.wallet_view, name='wallet'),  

]