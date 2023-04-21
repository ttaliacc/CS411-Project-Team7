from django import forms
from .models import Movie as Movie_Model

class add_movie_form(forms.ModelForm):
    class Meta:
        model = Movie_Model
        fields = '__all__'
