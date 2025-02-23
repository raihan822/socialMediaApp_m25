from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']

class PostFilterForm(forms.Form):
    SORT_CHOICES = [
        ('newest', 'Newest First'),
        ('oldest', 'Oldest First'),
    ]
    MEDIA_CHOICES = [
        ('all', 'All Posts'),
        ('text', 'Text Only'),
        ('image', 'With Images'),
    ]
    
    search = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Search posts...'}))
    sort = forms.ChoiceField(choices=SORT_CHOICES, required=False)
    media_type = forms.ChoiceField(choices=MEDIA_CHOICES, required=False)
    author = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Filter by author...'}))