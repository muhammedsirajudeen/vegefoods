from django.urls import path
from profile_app import views


urlpatterns = [
    path('user_account/',views.profile_view, name='profile_view'),
    path('user_account/update_profile/<int:user_id>/', views.update_profile, name='update_profile'),    

]