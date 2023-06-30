from django import forms
from authentication.admin import UserCreationForm, UserChangeForm
from authentication.models import *
from authentication.utils import *




class UpdateProfileForm(forms.ModelForm):
    
    email = forms.EmailField(

        validators=[checkemail], label='Email :', widget=forms.EmailInput(
        attrs={'id': 'email', 'class': 'email', 'placeholder': "Enter email"}), 
        error_messages={'required':"enter email"})
    
    first_name = forms.CharField(
        required=False, 
        
        validators=[checkalpha] , 
        label='First Name :', 
        widget=forms.TextInput(
        attrs={'id': 'f_name', 'class': 'f_name', 'placeholder': "First Name"}), 
        error_messages={'required':"Enter First Name"})
    
    last_name = forms.CharField(validators=[checkalpha] , label='Last Name :', widget=forms.TextInput(
        attrs={'id': 'l_name', 'class': 'l_name', 'placeholder': "Enter Last Name"}), 
        error_messages={'required':"Enter Last Name "})
    
    address = forms.CharField(label='Current City :', widget=forms.TextInput(
        attrs={'id': 'address', 'class': 'address_id', 'placeholder': "Enter Current City"}), 
        error_messages={'required':"City Is required "})
    
    phone = forms.CharField(validators=[checkphone], label='Phone Number :', widget=forms.TextInput(
        attrs={'id': 'phone', 'class': 'phone', 'placeholder': "Enter phone"}), 
        error_messages={'required':"Enter Phone Number"})

    class Meta:
        model = User 
        fields = ("first_name", "last_name", "email", "address","phone")

        

GENRE_CHOICE = [
    ('', ''),
    ('drama', 'Drama'),
    ('action', 'Action'),
    ('thriller', 'Thriller'),
    ('adventure', 'Adventure'),
    ('horror', 'Horror'),
    ('romance', 'Homance'),
    ('mystery', 'Hystery'),
]

LANGUAGE_CHOICE = [
     ('', ''),
    ('english', 'English'), 
    ('nepali', 'Nepali'), 
    ('hindi', 'Hindi'), 
]

class FilterMovieForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),required=False)
    genre = forms.MultipleChoiceField(choices= GENRE_CHOICE , required=False)
    language = forms.ChoiceField(choices= LANGUAGE_CHOICE , required=False)
    