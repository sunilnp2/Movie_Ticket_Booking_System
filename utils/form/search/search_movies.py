from django import forms
from movie.models import Movie


class SearchForm(forms.Form):
    search = forms.CharField(label='Search', max_length=100,empty_value="")
    queryset = Movie.objects.all()
    
    def filter_movie(self):
        search = self.cleaned_data.get('search')
        return self.queryset.filter(name__istartswith = search)
