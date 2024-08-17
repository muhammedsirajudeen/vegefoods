from django.shortcuts import render

# Create your views here.
def user_registration(request):
    return render(request,'signup.html')

def user_login(request):
    return render(request,'login.html')


def user_home(request):
    return render(request,'index.html')