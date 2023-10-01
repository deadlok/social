from django import forms
from .models import Post, Comment

class PostModelForm (forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows':2}))

    class Meta:
        model = Post
        fields = ('content','image')

class CommentModelForm(forms.ModelForm):
    body = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder':'Add comment ...', 'rows':1, 'class':'form-control'}))

    class Meta:
        model = Comment 
        fields = ('body',)

