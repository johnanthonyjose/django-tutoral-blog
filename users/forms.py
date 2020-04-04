from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email','password1','password2']


class UserUpdateForm(forms.ModelForm):
    '''
    Model Form
    A form that will work together specific database model
    In thise case, we want to create a model form that updates the database
    '''
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email']

        #Profile Picture is not here because that will be included in the profile model. not here
        # TODO: Why do you want it separate???
        # Answer: Because they're on a separate table in the database

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

        #Allow us to Update Profile Picture