from django.urls import path
from profile_app import views


urlpatterns = [
    path('user_account/',views.profile_view, name='profile_view')
    
    
]