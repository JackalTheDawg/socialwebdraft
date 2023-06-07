from django import forms
from django.forms import MultiWidget
from functional_app import models
from django.contrib.auth.models import User

class Sign_in_form(forms.Form):
    login = forms.CharField(max_length=12, widget=forms.TextInput(attrs={'placeholder': 'Login'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    required_css_class = "field"



class Create_user(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username',
                  'password',
                  'email')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Login'}),
            'password': forms.TextInput(attrs={'placeholder': 'Password'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email'})

        }

class Registarion_form(forms.ModelForm):
    class Meta:
        model = models.User_profile
        fields = ('profile_picture',
                  'first_name',
                  'second_name',
                  'sex',
                  'birthday',
                  'birthday_month',
                  'birthday_year')
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter your name'}),
            'second_name': forms.TextInput(attrs={'placeholder': 'Enter your second name'})
        }