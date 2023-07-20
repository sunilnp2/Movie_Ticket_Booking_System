from django.shortcuts import render, redirect
from django.views import View
from authentication.forms import SignupForm, LoginForm, EditUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from cinema.models import *
from cinema.views import BaseView
from authentication.models import User, Customer
from utils.forms import UpdateProfileForm
from authentication.tasks import activate_email

# Create your views here.
from django.contrib.auth.backends import ModelBackend

UserModel = get_user_model()

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None
  

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
        customer = Customer.objects.create(
            email = user.email,
            username = user.username,
            first_name = user.first_name,
            last_name = user.last_name,
            phone = user.phone,
            address = user.address,
            balance = 10000
        )
        customer.save()
        messages.success(request, "Thank you for your email confirmation you can login your account.")
        return redirect('authentication:login')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('home')

def activateEmail(request, user, to_email):
    id = user.id
    domain =  get_current_site(request).domain
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token =  account_activation_token.make_token(user)
    protocol = 'https' if request.is_secure() else 'http'
    # activate_url = f"{protocol}://{domain}/authentication/activate/{uid}/{token}"
    activate_email.delay(id, domain, uid, token, protocol)
    
    # mail_subject = "Activate your user account."
    # message = render_to_string("email-activate.html", {
    #     'user': user.first_name,
    #     'domain': get_current_site(request).domain,
    #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
    #     'token': account_activation_token.make_token(user),
    #     "protocol": 'https' if request.is_secure() else 'http'
    # })
    # email = EmailMessage(mail_subject, message, to=[to_email])
    # if email.send():
    messages.success(request, f' Dear {user.username}.Go to your email {to_email} and verify your email \
                If not found Check your spam folder.')
    # else:
    #     messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')



class LoginView(BaseView):
    def get(self,request):
        self.views['fm'] = LoginForm()
        return render(request, 'login.html', self.views)
    
    def post(self,request):
        email = request.POST.get('email')
        pw = request.POST.get('password')
        if not email:
            messages.error(request,"Email required")
        if not pw:
            messages.error(request,"Password required")
        user = authenticate(email = email, password = pw)
        if User.objects.filter(email = email, email_verified = False):
            messages.error(request, "You are not Verified! Verify email first")
            return redirect('authentication:login')
        if user is not None:
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            
            messages.success(request, "Login Successfully")
            return redirect('cinema:home')
        
        messages.error(request, "Enter Correct password")
        return render(request, 'login.html')


class SignupView(BaseView):  
    def get(self,request):
        self.views['fm'] = SignupForm()
        return render(request, 'signup.html', self.views)

    def post(self,request):
        fm = SignupForm(request.POST)
        if fm.is_valid():
            user = fm.save(commit=False)
            user.email_verified=False
            email = fm.cleaned_data['email']
            uname = email.split('@')[0]
            user.username = uname
            user.save()
            activateEmail(request, user, fm.cleaned_data.get('email'))
            fm.save()
            return redirect('cinema:home')
        return render(request, 'signup.html', {'fm': fm})
    

class ProfileView(BaseView):
    def get(self, request):
        user = request.user
        customer_id = Customer.objects.get(email = user.email)
        self.views['fm'] = UpdateProfileForm(instance=customer_id)
        
        return render(request, 'profile.html', self.views)


    def post(self, request):
        user = request.user
        customer = Customer.objects.get(email = user.email)
        fm = UpdateProfileForm(request.POST, instance=customer)
        if fm.is_valid():
            fm.save()
            messages.success(request, "Profile Update successfully")
            return redirect('authentication:profile')
        print(fm.errors)
        messages.error(request, "Some Error Occurs")
        return redirect('authentication:profile')



        
class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "Log Out success")
        return redirect('cinema:home')