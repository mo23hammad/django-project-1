from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile

class UserRegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='password',widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='confirm password',widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data['email']  # Use square brackets
        user_exists = User.objects.filter(email=email).exists()
        if user_exists:
            raise ValidationError('Email already exists. Please use a different email.')

        return email

    def clean_username(self):  # Corrected method name
        username = self.cleaned_data['username']  # Use square brackets
        username_exists = User.objects.filter(username=username).exists()
        if username_exists:
            raise ValidationError('Username already exists. Please choose a different one.')

        return username

    def clean(self):
        cd=super().clean()
        p1= cd.get('password1')
        p2= cd.get('password2')
        if p1 and p2 and p1 != p2:
            raise ValidationError('password must match')
        return cd
class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class EditProfileForm(forms.ModelForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = Profile
        fields = ('age','bio')


    
