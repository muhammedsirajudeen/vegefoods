from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.sessions.models import Session
# Create your views here.



@login_required(login_url='login')
@never_cache
def user_home(request):
    username = request.user.username
    return render(request, 'index.html',{'username': username})


def user_registration(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            print("Passwords do not match")
   
            return render(request, 'signup.html', {'error': 'Passwords do not match'})

        user = User.objects.create_user(username=uname, first_name=first_name, last_name=last_name, email=email, password=pass1)
        user.save()
        return redirect('login')  # Corrected redirect usage

    return render(request, 'signup.html')
    
@never_cache 
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        print(username,pass1)
        user = authenticate(request,username = username,password = pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            print("wrong")
    return render(request,'login.html')


def user_logout(request):
  
    logout(request)
   
    return redirect('login')



