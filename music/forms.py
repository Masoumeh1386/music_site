from django import forms
from .models import Song,Comment


class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'artist', 'audio_file', 'cover', 'description', 'release_date']
        widgets = {
            'release_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'جستجو در آهنگ‌ها...',
            'class': 'form-control',
        })
    )




class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'نظرت رو بنویس...'}),
        }