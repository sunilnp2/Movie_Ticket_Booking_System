from django import forms
from cinema.admin import UserCreationForm
from cinema.models import *

def checkalpha(value):
    # if value.startswith("," | "!" | "." | "/" | "<" | ">" | "{"):
        # raise forms.ValidationError("This is invalid")
    if value.isalpha() == False:
        raise forms.ValidationError('This is Invalid.')

def checkuserame(value):
    if value.isalnum() == False:
        raise forms.ValidationError('Username should be alpha or digit only.!')


def checkemail(value):
    if User.objects.filter(email = value).exists():
        raise forms.ValidationError("This email is already taken try another")
    if value.endswith('.com') == False:
        raise forms.ValidationError("Enter a valid email")
    
def checkphone(value):
    if value.isdigit() == False or len(value) < 10:
        raise forms.ValidationError("Phone number must be in digits and 10 numbers")

class SignupForm(UserCreationForm):
    password1 = forms.CharField(label='Enter Password:',
                                widget=forms.PasswordInput(
                                    attrs={'class': 'input'}),
                                error_messages={'required': 'This Password is required'})
    password2 = forms.CharField(label='Confirm Password',
                                widget=forms.PasswordInput(attrs={'placeholder': "confirm password",
                                                                  'class': 'password2', 'id': 'cpassword'}),
                                error_messages={'required': "Enter confirm password"})
    
    email = forms.EmailField(validators=[checkemail], label='Email :', widget=forms.EmailInput(
        attrs={'id': 'email', 'class': 'email', 'placeholder': "Enter email"}), 
        error_messages={'required':"enter email"})
    
    first_name = forms.CharField(validators=[checkalpha] , label='First Name :', widget=forms.TextInput(
        attrs={'id': 'f_name', 'class': 'f_name', 'placeholder': "First Name"}), 
        error_messages={'required':"Enter First Name"})
    
    last_name = forms.CharField(validators=[checkalpha] , label='Last Name :', widget=forms.TextInput(
        attrs={'id': 'l_name', 'class': 'l_name', 'placeholder': "Enter Last Name"}), 
        error_messages={'required':"Enter Last Name "})
    
    phone = forms.CharField(validators=[checkphone], label='Phone Number :', widget=forms.TextInput(
        attrs={'id': 'phone', 'class': 'phone', 'placeholder': "Enter phone"}), 
        error_messages={'required':"Enter Phone Number"})

    class Meta:
        model = User 
        fields = ("email", "first_name", "last_name","phone")


class LoginForm(forms.ModelForm):
    email = forms.EmailField(label='Email :', widget=forms.EmailInput(
        attrs={'id': 'email', 'class': 'email', 'placeholder': "Enter email"}), 
        error_messages={'required':"enter email"})
    
    password1 = forms.CharField(label='Enter Password :',
                                widget=forms.PasswordInput(
                                    attrs={'class': 'input', 'placeholder':'Enter password'}),
                                error_messages={'required': 'This Password is required'})

    class Meta:
        model = User
        fields = ('email', 'password1')


# form for showtime custom editing ----------------------------------------------------------------
