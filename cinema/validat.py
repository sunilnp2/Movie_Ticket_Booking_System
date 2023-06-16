# from django import forms
# from cinema.models import *


# def checkalpha(value):
    
#     # if value.startswith("," | "!" | "." | "/" | "<" | ">" | "{"):
#         # raise forms.ValidationError("This is invalid")
#     if value.isalpha() == False:
#         raise forms.ValidationError('This is Invalid.')

# def checkuserame(value):
#     if value.isalnum() == False:
#         raise forms.ValidationError('Username should be alpha or digit only.!')


# def checkemail(value):
#     if User.objects.filter(email = value).exists():
#         raise forms.ValidationError("This email is already taken try another")
#     if value.endswith('.com') == False:
#         raise forms.ValidationError("Enter a valid email")
    
# def checkphone(value):
#     if value.isdigit() == False or len(value) < 10:
#         raise forms.ValidationError("Phone number must be in digits and 10 numbers")