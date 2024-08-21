from django.shortcuts import render,redirect
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.sessions.models import Session
from django.core.mail import send_mail
from django.conf import settings
from . models import  OTP

import random
# Create your views here.


def redirect_to_home(request):
    return redirect('home')

@never_cache
def user_home(request):
    username = request.user.username
    return render(request, 'user/index.html',{'username': username})


def user_registration(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            return render(request, 'user/signup.html', {'error': 'Passwords do not match'})
        user = User.objects.create_user(username=uname, first_name=first_name, last_name=last_name, email=email, password=pass1)
        user.save()

        # Create and send OTP
        otp = OTP(user=user)
        otp.save()
        send_otp_via_email(email, otp.otp_code)
        return redirect('verify_otp',user_id=user.id)  # Corrected redirect usage

    return render(request, 'user/signup.html')

def send_otp_via_email(email, otp_code):
    subject = 'Your OTP Code'
    message = f'Your OTP code is {otp_code}.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)



from django.contrib.auth import login
from django.contrib.auth.backends import ModelBackend

def verify_otp(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        if request.method == 'POST':
            entered_otp = ''.join([request.POST.get(f'otp{i+1}') for i in range(6)])
            otp_record = OTP.objects.get(user=user)

            if otp_record.otp_code == entered_otp and otp_record.is_valid():
                user.is_active = True
                user.save()
                otp_record.delete()

                # Log the user in with the correct backend
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')

                return redirect('home')
            else:
                return render(request, 'user/otp.html', {'error': 'Invalid OTP or OTP expired'})

    except User.DoesNotExist:
        return redirect('home')

    return render(request, 'user/otp.html')
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
    return render(request,'user/login.html')


def user_logout(request):
  
    logout(request)
    return redirect('home')



class CustomPasswordResetView(PasswordResetView):
    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            return render(self.request, 'user/password_reset_form.html', {
                'form': form,
                'error': 'No account found with this email address.'
            })
        return super().form_valid(form)
