from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:  
            login(request, user)
            return redirect('panel')  
        else:
            # Handle invalid login
            return render(request, 'admin/admin_login.html', {'error': 'Invalid credentials or access denied'})
    return render(request, 'admin/admin_login.html')

def panel(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('admin/admin_login')  
    return render(request, 'admin/dashboard.html')  

def user_managment(request):
    users = User.objects.filter(is_superuser =  False).order_by('username')
    return render(request,'admin/users.html',{'users':users})




