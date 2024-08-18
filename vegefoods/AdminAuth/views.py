from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login

# Create your views here.
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:  # Ensure user is staff/admin
            login(request, user)
            return redirect('panel')  # Redirect to admin panel page
        else:
            # Handle invalid login
            return render(request, 'admin_login.html', {'error': 'Invalid credentials or access denied'})
    return render(request, 'admin_login.html')

def panel(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('admin_login')  # Redirect to login if not authenticated or not staff
    return render(request, 'dashboard.html')  # Replace with actual panel template
