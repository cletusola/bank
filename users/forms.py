from django import forms 
from django.contrib.auth import get_user_model
User = get_user_model()
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User




""" sign in form """
class LogInForm(forms.Form):
    username = forms.CharField(max_length=20, required=True)
    password = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput)


