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
    
    def filter_movie(self):
        movies = Movie.objects.all()
        start_date = self.cleaned_data['start_date']
        end_date = self.cleaned_data['end_date']
        genre = self.cleaned_data['genre']
        language = self.cleaned_data['language']
        if len(genre) == 0 or genre == None:
            pass
        else:
            genre = [g for g in genre]
            
        q_objects = Q()
        for g in genre:
            q_objects |= Q(genre__icontains=g)
            
        if start_date:
                print("start date: %s" % start_date)
                return movies.filter(
                    release_date__gte=start_date)
        elif end_date:
                print("start date: %s" % end_date)
                return movies.filter(
                    end_date__lte=end_date)

        elif genre and language:
                return movies.filter(
                   q_objects, language__icontains=language)
                
        elif genre:
            return movies.filter(q_objects)
                
        elif language is not None and language:
            print("I found language: %s" % language)
            return movies.filter(language__icontains=language)
    