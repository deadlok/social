from django import forms
from .models import Post, Comment
from django.forms import ValidationError

class PostModelForm (forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows':2}))

    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if image:
            if image.size > 1024*1024:
                raise ValidationError("Image file too large ( > 1mb )")
            return image
        else:
            raise ValidationError("Couldn't read uploaded image")
    
    class Meta:
        model = Post
        fields = ('content','image')

class CommentModelForm(forms.ModelForm):
    body = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder':'Add comment ...', 'rows':1, 'class':'form-control'}))

    class Meta:
        model = Comment 
        fields = ('body',)

