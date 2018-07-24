from django import forms
from .models import Profile, Image, Comment

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image', 'image_name', 'image_caption')
        # fields is the opposite of exclude

class ProfileUpdateForm(forms.Form):
    profile_name = forms.CharField(max_length=30,)
    profile_photo = forms.ImageField()
    bio = forms.CharField()

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)

class CaptionUpdateForm(forms.Form):
    image_caption = forms.CharField()
