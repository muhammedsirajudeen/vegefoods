from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.models import User

# Create your views here.
def profile_view(request):
    return render(request,"user/profile_app/profile.html")


def update_profile(request,user_id):
    user =  get_object_or_404(User,id=user_id)
    if request.method =="POST":
        username =  request.POST.get("username")
        email =  request.POST.get("email")
        new_password = request.POST.get("password")

        user.username = username
        user.email = email
        if new_password:
            user.set_password(new_password)

        user.save()
        return redirect('profile_view')
    return render(request,"user/profile_app/update_profile.html")
