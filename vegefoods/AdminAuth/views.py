from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login,logout
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
    if not request.user.is_authenticated or not request.user.is_superuser: 
        return redirect('admin_login')  # Use the correct URL name
    return render(request, 'admin/dashboard.html')  

 
def user_managment(request):  # Fixed name here
    if not request.user.is_authenticated or not request.user.is_superuser:  
        return redirect('admin_login') 
    users = User.objects.filter(is_superuser =  False).order_by('username')
    return render(request,'admin/users.html',{'users':users})


def block_unblock_user(request, user_id):
    if not request.user.is_authenticated or not request.user.is_superuser:  # Added authentication check
        return redirect('admin_login') # Redirect if the user is not an admin

    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'block':
            user.is_active = False
        elif action == 'unblock':
            user.is_active = True
        user.save()

    return redirect('user_management')  

def admin_logout(request):
    logout(request)
    return redirect('admin_login')

