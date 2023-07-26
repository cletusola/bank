from django import forms 
from django.contrib.auth import get_user_model
User = get_user_model()
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


import re 


""" sign in form """
class LogInForm(forms.Form):
    username = forms.CharField(max_length=20, required=True)
    password = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput)


    # clean username 
    def clean_username(self):
        # convert user name to lowercase ( to make it case insensitive)
        username = self.cleaned_data["username"].lower()

        return username 


""" Change password form """
class ChangePassword(forms.Form):
    current_password = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput)
    new_password = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput)
    new_password_again = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput)


    # clean password 
    def clean_new_password_again(self):
        new_password = self.cleaned_data["new_password"]
        new_password_again = self.cleaned_data["new_password_again"]

        if new_password == " " or new_password_again == " ":
            raise forms.ValidationError("Password is required")
        
        elif len(new_password) < 8 or len(new_password) > 30:
            raise forms.ValidationError("Password must be between 8 to 30 characters")

        elif not re.search("[@_!#$%^&*()-<>?/\|}={+~:]", new_password):
            raise forms.ValidationError("Password must contain at least one special character")
        
        elif not any(p.isupper() for p in new_password):
            raise forms.ValidationError("Password must contain at least one uppercase(capital letter)")
        
        elif not any(p.islower() for p in new_password):
            raise forms.ValidationError("Password must contain at least on lowercase(small letter)")
        
        elif not any(p.isdigit() for p in new_password):
            raise forms.ValidationError("Password must contain at least one digit(number)")

        elif new_password and new_password_again and new_password != new_password_again:
            raise forms.ValidationError("Passwords do not match")
        

        return new_password_again       