from django import forms
from authentication.admin import UserCreationForm, UserChangeForm
from authentication.models import *
from authentication.utils import *
from movie.models import Movie
from django.db.models import Q



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
    
    def get_filtered_data(self):
        return dict(
            filter(lambda item: item[1], self.cleaned_data.items()))

    def filter_movie(self):
        movies = Movie.objects.all()
        filter_data = self.get_filtered_data()
        genre = filter_data.get('genre')        
        q_objects = Q()
        if genre:
            for g in genre:
                q_objects |= Q(genre__icontains=g)
        qyeryset = movies.filter(**filter_data)
        return qyeryset.union(movies.filter(q_objects))