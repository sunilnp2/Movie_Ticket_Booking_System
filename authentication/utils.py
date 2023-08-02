from django import forms
from authentication.models import *


def checkalpha(value):
    
    # if value.startswith("," | "!" | "." | "/" | "<" | ">" | "{"):
        # raise forms.ValidationError("This is invalid")
    if value.isalpha() == False:
        raise forms.ValidationError('This is Invalid.')
    
def checkpassword(value):
    if len(value) <= 6:
        raise forms.ValidationError('Password Lenth must be greater than six.!')
    elif value[1].upper() == False:
        raise forms.ValidationError('First length must be capital!')
        

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
    
    elif  value.startswith('98') == False and value.startswith('97') == False:
        raise forms.ValidationError("Phone Number Must start with 98 or 97")