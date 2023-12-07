from django import forms
from authentication.admin import UserCreationForm, UserChangeForm
from authentication.models import *
from authentication.utils import *
from movie.models import Movie
from django.db.models import Q



class UpdateProfileForm(forms.ModelForm):
    
    email = forms.EmailField(

        validators=[checkemail], label='Email :', widget=forms.EmailInput(
        attrs={'id': 'email', 'class': 'email','readonly': 'readonly', 'placeholder': "Enter email"}), 
        error_messages={'required':"enter email"})
    
    username = forms.CharField(

        validators=[checkemail], label='Username :', widget=forms.TextInput(
        attrs={'id': 'email', 'class': 'email','readonly': 'readonly', 'placeholder': "Enter Username"}), 
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
        attrs={'id': 'address', 'class': 'address_id','readonly': 'readonly',  'placeholder': "Enter Current City"}), 
        error_messages={'required':"City Is required "})
    
    phone = forms.CharField(validators=[checkphone], label='Phone Number :', widget=forms.TextInput(
        attrs={'id': 'phone', 'class': 'phone','readonly': 'readonly',  'placeholder': "Enter phone"}), 
        error_messages={'required':"Enter Phone Number"})
    
    balance = forms.CharField(validators=[checkphone], label='Available Balance :', widget=forms.TextInput(
        attrs={'id': 'phone', 'class': 'phone','readonly': 'readonly', 'placeholder': "Enter phone"}), 
        error_messages={'required':"Enter Phone Number"})
    
    
    
    class Meta:
        model = Customer
        fields = '__all__'
    
    # def __init__(self, *args, **kwargs):
    #     instance = kwargs.get('instance')
    #     if instance:
    #         kwargs['initial'] = {
    #             'email': instance.email,
    #             'first_name': instance.first_name,
    #             'last_name': instance.last_name,
    #             'address': instance.address,
    #             'phone': instance.phone,
    #         }
    #     super(UpdateProfileForm, self).__init__(*args, **kwargs)
    
    # def save(self, commit=True):
    #     instance = self.instance
    #     instance.email = self.cleaned_data['email']
    #     instance.first_name = self.cleaned_data['first_name']
    #     instance.last_name = self.cleaned_data['last_name']
    #     instance.address = self.cleaned_data['address']
    #     instance.phone = self.cleaned_data['phone']
    #     if commit:
    #         instance.save()
    #     return instance

        

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