from django import forms
from .models import MovieRequest, Petition

class MovieRequestForm(forms.ModelForm):
    class Meta:
        model = MovieRequest
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter movie name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter movie description'}),
        }
        labels = {
            'name': 'Movie Name',
            'description': 'Movie Description',
        }

class PetitionForm(forms.ModelForm):
    class Meta:
        model = Petition
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter petition title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Describe why this movie should be added to the catalog'}),
        }
        labels = {
            'title': 'Petition Title',
            'description': 'Petition Description',
        }
