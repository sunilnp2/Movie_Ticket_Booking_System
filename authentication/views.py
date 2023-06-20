from django.shortcuts import render, redirect
from django.views import View
from authentication.forms import SignupForm, LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from cinema.models import *
from datetime import date
from django.http import HttpResponse
from cinema.views import BaseView

# Create your views here.


from .tokens import account_activation_token

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.email_verified = True
        user.save()

        messages.success(request, "Thank you for your email confirmation you can login your account.")
        return redirect('authentication:login')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('home')

def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("email-activate.html", {
        'user': user.first_name,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f' Dear {user.first_name}.Go to your email {to_email} and verify your email \
                If not found Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')



class LoginView(BaseView):
    def get(self,request):
        self.views['fm'] = LoginForm()
        return render(request, 'login.html', self.views)
    
    def post(self,request):
        email = request.POST.get('email')
        pw = request.POST.get('password')
        if not email:
            messages.error(request,"Username required")
        if not pw:
            messages.error(request,"Username required")
        user = authenticate(email = email, password = pw)
        if user is not None:
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            
            messages.success(request, "Login Successfully")
            return redirect('cinema:home')
        
        messages.error(request, "Enter Correct password")
        return render(request, 'login.html')


class SignupView(BaseView):
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            return self.get(request, *args, **kwargs)
        elif request.method == 'POST':
            return self.post(request, *args, **kwargs)
        else:
            return HttpResponse(['GET', 'POST']) 
        
    def get(self,request):
        self.views['fm'] = SignupForm()
        return render(request, 'signup.html', self.views)

    def post(self,request):
        fm = SignupForm(request.POST)
        if fm.is_valid():
            user = fm.save(commit=False)
            user.email_verified=False
            user.save()
            activateEmail(request, user, fm.cleaned_data.get('email'))
            fm.save()
            return redirect('cinema:home')
        return render(request, 'signup.html', {'fm': fm})


        
class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "Log Out success")
        return redirect('cinema:home')