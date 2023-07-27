from django import forms 
from django.contrib.auth import get_user_model
User = get_user_model()
# from django.core.exceptions import ValidationError

from .models import Account

import re 



""" Account form ... open account and register form """

# This form contains basic account information 
class AccountInformationForm(forms.Form):
    acc_type = (
        ('savings','savings'),
        ('checkings','checkings')
    )
    first_name = forms.CharField(max_length=30, min_length=2, required=True)
    last_name = forms.CharField(max_length=30, min_length=2, required=True)
    phone = forms.CharField(min_length=5, max_length=14, required=True)
    address = forms.CharField(max_length=80, required=True)
    occupation = forms.CharField(max_length=60, required=True)
    account_type = forms.CharField(max_length=20, required=True)

    """ cleaning form fields """

    #clean firstname
    def clean_first_name(self):
        first_name = self.cleaned_data['first_name'].lower()
        
        if len(first_name) < 2 or len(first_name) > 30:
            raise forms.ValidationError("Name must be between 2 to 30 characters")
        
        elif first_name == " ":
            raise forms.ValidationError("Name cannot be empty")
        
        elif re.search("[@_!#$%^&*()-<>?/\|}={+~:]", first_name):
            raise forms.ValidationError("Name cannot contain special characters")
        
        else:
            pass 

        return first_name

    #clean lastname
    def clean_last_name(self):
        last_name = self.cleaned_data['last_name'].lower()
        
        if len(last_name) < 2 or len(last_name) > 30:
            raise forms.ValidationError("Name must be between 2 to 30 characters")
        
        elif last_name == " ":
            raise forms.ValidationError("Name cannot be empty")
        
        elif re.search("[@_!#$%^&*()-<>?/\|}={+~:]", last_name):
            raise forms.ValidationError("Name cannot contain special characters")
        
        else:
            pass 

        return last_name

    #clean phone
    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        chk_phone = Account.objects.filter(account_phone=phone)

        if chk_phone.count():
            raise forms.ValidationError("A user with that phone number already exist")
        
        elif re.search("[@_!#$%^&*<>?/\|}={~:]", phone):
            raise forms.ValidationError("Phone can not contain special characters")

        elif not all(t.isdigit() for t in phone):
            raise forms.ValidationError("Phone can only contian numbers")
        
        elif len(phone) < 5 or len(phone) > 14:
            raise forms.ValidationError("Phone must be between 5 to 14 characters")
        
        elif phone == " ":
            raise forms.ValidationError("Phone is required")

        else:
            pass
        
        return phone

    #clean address
    def clean_address(self):
        address = self.cleaned_data['address']
        
        if len(address) > 80:
            raise forms.ValidationError("Address cannot be more than 80 characters")
        
        elif address == " ":
            raise forms.ValidationError("Address cannot be empty")
        
        elif re.search("[@!$%^&*()<>?/\|}={~:]", address):
            raise forms.ValidationError("Address cannot contain special characters")
        
        else:
            pass 

        return address

    #clean occupation
    def clean_occupation(self):
        occupation = self.cleaned_data['occupation']
        
        if len(occupation) > 60:
            raise forms.ValidationError("Occupation cannot be more than 60 characters")
        
        elif occupation == " ":
            raise forms.ValidationError("Occupation cannot be empty")
        
        elif re.search("[@_!$%^&*()<>?/\|}={+~:]", occupation):
            raise forms.ValidationError("Occupation cannot contain special characters")
        
        else:
            pass 

        return occupation

    """ cleaning form fields end"""


# This form contains user information which will be used for further authentication 
class UserInformationForm(forms.Form):
    username = forms.CharField(min_length=5, max_length=20, required=True)
    email = forms.EmailField(min_length=6, max_length=60, required=True)
    password1 = forms.CharField(min_length=8, max_length=30,required=True,
                                widget=forms.PasswordInput)
    password2 = forms.CharField(min_length=8, max_length=30,required=True,
                                widget=forms.PasswordInput)
    transaction_pin = forms.CharField(min_length=4, max_length=6,required=True,
                                widget=forms.PasswordInput)


    """ cleaning form fields """

    # clean username 
    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        chk_username = User.objects.filter(username = username)

        if chk_username.count():
            raise forms.ValidationError(f"Username {username} is unavailable")
        
        elif username == " ":
            raise forms.ValidationError("Username cannot be empty")
        
        elif len(username) < 5 or len(username) > 20:
            raise forms.ValidationError("Username must be between 4 to 20 characters")
        
        elif re.search("[@!#$%^&*()<>?/\|}={+~:]", username):
            raise forms.ValidationError("Only '_' and '-' are allowed in username. ")
        
        elif " " in username.strip():
            username = username.replace(" ","_")

        return username
    
    # clean email 
    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        chk_email = User.objects.filter(email = email)

        if chk_email.count():
            raise forms.ValidationError(f"Email {email} is unavailable")
        
        elif email == " ":
            raise forms.ValidationError("Email cannot be empty")
        
        elif len(email) < 6 or len(email) > 60:
            raise forms.ValidationError("Email must be between 6 to 60 characters")
        
        return email
    

    # clean password
    def clean_password2(self):
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]

        if password1 == " " or password2 == " ":
            raise forms.ValidationError("Password is required")
        
        elif len(password1) < 8 or len(password1) > 30:
            raise forms.ValidationError("Password must be between 8 to 30 characters")

        elif not re.search("[@_!#$%^&*()-<>?/\|}={+~:]", password1):
            raise forms.ValidationError("Password must contain at least one special character")
        
        elif not any(p.isupper() for p in password1):
            raise forms.ValidationError("Password must contain at least one uppercase(capital letter)")
        
        elif not any(p.islower() for p in password1):
            raise forms.ValidationError("Password must contain at least on lowercase(small letter)")
        
        elif not any(p.isdigit() for p in password1):
            raise forms.ValidationError("Password must contain at least one digit(number)")

        elif password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        

        return password2
    
    # clean transaction pin
    def clean_transaction_pin(self):
        transaction_pin = self.cleaned_data["transaction_pin"]

        if not re.search("[@_!#$%^&*()-<>?/\|}={+~:]", transaction_pin):
            # raise forms.ValidationError("Transaction pin can not contain special characters")
            pass
        
        elif not all(t.isdigit() for t in transaction_pin):
            raise forms.ValidationError("Transaction pin can only contian numbers")
        
        elif len(transaction_pin) < 4 or len(transaction_pin) > 6:
            raise forms.ValidationError("Transaction pin must be between 4 to 6 characters")
        
        elif transaction_pin == " ":
            raise forms.ValidationError("Transaction pin is required")

        else:
            pass

        return transaction_pin
    

    """ cleaning form fields ends """

""" Account form ... open account and register form  ends """


""" Money Transfer  form """
class TransferForm(forms.Form):
    account = forms.CharField(max_length=15, required=True)
    amount = forms.CharField(min_length=1, required=True)

    #clean account
    def clean_account(self):
        account = self.cleaned_data["account"]
        
        if not all(r.isdigit() for r in account):
            raise forms.ValidationError("Account number can only be numbers")
        elif account == " ":
            raise forms.ValidationError("Account number cannot be empty")
        else:
            pass 

        return account

 
    #clean amount
    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        
        if not all(r.isdigit() for r in amount):
            raise forms.ValidationError("Invalid amount")
        elif amount == " ":
            raise forms.ValidationError("Amount cannot be empty")
        else:
            pass 

        return amount


""" Money Transfer form ends """

""" change transaction pin """
class ChangePinForm(forms.Form):
    pin = forms.CharField(min_length=4, max_length=6, required=True)
    pin2 = forms.CharField(min_length=4, max_length=6, required=True)


    # clean transaction pin
    def clean_pin2(self):
        pin = self.cleaned_data["pin"]
        pin2 = self.cleaned_data["pin2"]

        if pin != pin2:
            raise forms.ValidationError("pin must match")
        
        elif not re.search("[@_!#$%^&*()-<>?/\|}={+~:]", pin):
            # raise forms.ValidationError("Transaction pin can not contain special characters")
            pass
        
        elif not all(t.isdigit() for t in pin):
            raise forms.ValidationError("Transaction pin can only contian numbers")
        
        elif len(pin) < 4 or len(pin) > 6:
            raise forms.ValidationError("Transaction pin must be between 4 to 6 characters")
        
        elif pin == " " or pin2 == " ":
            raise forms.ValidationError("Transaction pin is required")

        else:
            pass

        return pin2
    

""" Update user information """
class UserInfoForm(forms.ModelForm):
    username = forms.CharField(min_length=5, max_length=20, required=True)
    email = forms.EmailField(min_length=6, max_length=60, required=True)

    class Meta:
        model = User 
        fields = ["username", "email"]

    # clean username 
    def clean_username(self):
        username = self.cleaned_data["username"].lower()
        # fetch current user
        user_username = self.instance.username
        #check if new username is available
        chk_username = User.objects.filter(username=username)

        if username != user_username and chk_username.count():
            raise forms.ValidationError(f"Username {username} is not available")
        
        elif username == " ":
            raise forms.ValidationError("Username cannot be empty")
        
        elif len(username) < 5 or len(username) > 20:
            raise forms.ValidationError("Username must be between 4 to 20 characters")
        
        elif re.search("[@!#$%^&*()<>?/\|}={+~:]", username):
            raise forms.ValidationError("Only '_' and '-' are allowed in username. ")
        
        elif " " in username.strip():
            username = username.replace(" ","_")

        return username
    
    # clean email
    def clean_email(self):
        email = self.cleaned_data["email"]
        #fetch current user
        user_email = self.instance.email
        # check if new email is available  
        chk_email = User.objects.filter(email=email)

        if email != user_email and chk_email.count():
            raise forms.ValidationError(f"Email {email} is not available")
        
        elif email == " ":
            raise forms.ValidationError("Email cannot be empty")
        
        elif len(email) < 6 or len(email) > 60:
            raise forms.ValidationError("Email must be between 6 to 60 characters")
        
        return email
    

""" update profile information """
class ProfileInfoForm(forms.ModelForm):
    account_phone = forms.CharField(min_length=5, max_length=14, required=True)
    account_address = forms.CharField(max_length=80, required=True)
    account_occupation = forms.CharField(max_length=60, required=True)

    class Meta:
        model = Account 
        fields = ["account_phone","account_address","account_occupation"]


    # clean phone 
    def clean_account_phone(self):
        account_phone = self.cleaned_data["account_phone"]

        phone = self.instance.account_phone
        # check if phone number is available
        chk_phone = Account.objects.filter(account_phone=account_phone)

        if account_phone != phone and chk_phone.count():
            raise forms.ValidationError(f"Phone number {account_phone} is unavailable")
        
        elif re.search("[@_!#$%^&*<>?/\|}={~:]", account_phone):
            raise forms.ValidationError("Phone can not contain special characters")

        elif not all(t.isdigit() for t in account_phone):
            raise forms.ValidationError("Phone can only contian numbers")
        
        elif len(account_phone) < 5 or len(account_phone) > 14:
            raise forms.ValidationError("Phone must be between 5 to 14 characters")
        
        elif account_phone == " ":
            raise forms.ValidationError("Phone is required")

        else:
            pass
        
        return account_phone 
    
    #clean address
    def clean_account_address(self):
        account_address = self.cleaned_data['account_address']
        
        if len(account_address) > 80:
            raise forms.ValidationError("Address cannot be more than 80 characters")
        
        elif account_address == " ":
            raise forms.ValidationError("Address cannot be empty")
        
        elif re.search("[@!$%^&*()<>?/\|}={~:]", account_address):
            raise forms.ValidationError("Address cannot contain special characters")
        
        else:
            pass 

        return account_address

    #clean occupation
    def clean_account_occupation(self):
        account_occupation = self.cleaned_data['account_occupation']
        
        if len(account_occupation) > 60:
            raise forms.ValidationError("Occupation cannot be more than 60 characters")
        
        elif account_occupation == " ":
            raise forms.ValidationError("Occupation cannot be empty")
        
        elif re.search("[@_!$%^&*()<>?/\|}={+~:]", account_occupation):
            raise forms.ValidationError("Occupation cannot contain special characters")
        
        else:
            pass 

        return account_occupation
