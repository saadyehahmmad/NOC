from PIL import Image
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    user_type = forms.ChoiceField(choices=Profile.USER_TYPE_CHOICES)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'user_type']

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        if commit:
            user.save()
            Profile.objects.create(user=user, user_type=self.cleaned_data.get('user_type'))
        return user


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)


class ProfileUpdateForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput(), required=False)
    y = forms.FloatField(widget=forms.HiddenInput(), required=False)
    width = forms.FloatField(widget=forms.HiddenInput(), required=False)
    height = forms.FloatField(widget=forms.HiddenInput(), required=False)
    facebook_link = forms.URLField(required=False)
    twitter_link = forms.URLField(required=False)
    instagram_link = forms.URLField(required=False)
    linkedin_link = forms.URLField(required=False)
    image = forms.ImageField(label=('Image'), error_messages={'invalid': ("Image files only")}, widget=forms.FileInput, required=False)

    class Meta:
        model = Profile
        fields = ['bio', 'date_of_birth', 'image', 'user_type','facebook_link', 'twitter_link', 'instagram_link', 'linkedin_link']

    def save(self, *args, **kwargs):
        profile = super(ProfileUpdateForm, self).save(*args, **kwargs)

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        if x and y and w and h:
            image = Image.open(profile.image)
            cropped_image = image.crop((x, y, w + x, h + y))
            resized_image = cropped_image.resize((300, 300), Image.ANTIALIAS)
            resized_image.save(profile.image.path)

        return profile
