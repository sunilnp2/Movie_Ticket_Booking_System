from django import forms
from authentication.admin import UserCreationForm, UserChangeForm
from authentication.models import *
from authentication.utils import *


ADDRESS_CHOICES = [
    ('Kathmandu', 'Kathmandu'),
    ('Pokhara', 'Pokhara'),
    ('Butwal', 'Butwal'),
    ('Dharan', 'Dharan'),
    ('Bhaktpur', 'Bhaktpur'),
    ('LalitPur', 'Lalitpur'),
]

class SignupForm(UserCreationForm):
    password1 = forms.CharField(label='Enter Password:',validators=[checkpassword],
                                widget=forms.PasswordInput(
                                    attrs={'class': 'input'}),
                                error_messages={'required': 'This Password is required'})
    password2 = forms.CharField(label='Confirm Password',
                                widget=forms.PasswordInput(attrs={'placeholder': "confirm password",
                                                                  'class': 'password2', 'id': 'cpassword'}),
                                error_messages={'required': "Enter confirm password"})
    
    email = forms.EmailField(

        validators=[checkemail], label='Email :', widget=forms.EmailInput(
        attrs={'id': 'email', 'class': 'email', 'placeholder': "Enter email"}), 
        error_messages={'required':"enter email"})

    
    # address = forms.CharField(label='Current City :', widget=forms.TextInput(
    #     attrs={'id': 'address', 'class': 'address_id', 'placeholder': "Enter Current City"}), 
    #     error_messages={'required':"City Is required "})
    
    address = forms.ChoiceField(choices=ADDRESS_CHOICES, label='Current City :',
        error_messages={'required':"City Is required "})
    
    phone = forms.CharField(validators=[checkphone], label='Phone Number :', widget=forms.TextInput(
        attrs={'id': 'phone', 'class': 'phone', 'placeholder': "Enter phone"}), 
        error_messages={'required':"Enter Phone Number"})

    class Meta:
        model = User 
        fields = ("email", "address","phone")


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

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email','username', 'first_name', 'last_name', 'phone', 'address'] 