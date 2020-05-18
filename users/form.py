from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class RegisterForm(UserCreationForm):
    # email isn't a default field in the User model so it needs to be added manually
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class RegisterUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

