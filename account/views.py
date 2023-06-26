from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
User = get_user_model()

from .forms import (
    AccountInformationForm,
    UserInformationForm,
)

from .models import (
    Account,
    Account_History
)

import random 



# function to generate account number 
def generate_account_number():

    gen_rand = random.randrange(0000000, 9999999, 7)
    account_identifier = 23 

    account_number_string = str(account_identifier) + str(gen_rand)
    account_number_int = int(account_number_string)

    return account_number_int


""" Account opening and registration view """

# account info view
def register_account(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == "POST":
        form = AccountInformationForm(request.POST)
        if form.is_valid():
            request.session['first_name'] = form.cleaned_data('first_name')
            request.session['last_name'] = form.cleaned_data('last_name')
            request.session['phone'] = form.cleaned_data('phone')
            request.session['address'] = form.cleaned_data('address')
            request.session['occupation'] = form.cleaned_data('occupation')
            request.session['account_type'] = form.cleaned_data('account_type')

            return redirect('user_info')
        
        else:
            messages.error(request, "Please make sure you provide correct information")
            return render(request, 'join/register.html', context={'form':form})
    else:
        form = AccountInformationForm()
        return render(request, 'join/register.html', context={'form':form})


# user info view -- this is where we will perform account opening and user registration 
def user_info(request):
    if request.method == 'POST':
        form = UserInformationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data('username')
            email = form.cleaned_data('email')
            password = form.cleaned_data('password2')
            transaction_pin = form.cleaned_data('transaction_pin')

            user = User.objects.create_user(
                first_name = request.session['first_name'],
                last_name = request.session['last_name'],
                username = username,
                email = email,
                password = password
            )
            user.save()

            try:
                account = Account.objects.create(
                    account_number = generate_account_number(),
                    account_owner = user,
                    account_type = request.session['account_type'],
                    account_address = request.session['address'],
                    account_phone = request.session['phone'],
                    account_occupation = request.session['occupation'],
                    transaction_pin = transaction_pin
                )
                account.save()
                return redirect('dashboard')
            
            except:
                messages.error(request, "Unable to create account, please contact our customer service with user user information(username and email)")

        else:
            messages.error(request, "Please provide accurate informations")
            return render(request, 'join/user_info.html', context={'form':form})

    else:
        form = UserInformationForm()
        return render(request, 'join/user_info.html', context={'form':form})


""" Account opening and registration view ends """

""" Account View """

# account profile view 
@login_required(login_url='login')
def dashboard(request):
    profile = Account.objects.filter(account_owner=request.user)
    return render(request, 'pages/dashboard.html', context={'profile':profile})

""" Account view ends"""



""" (Transaction) Money Transfer view """




""" (Transaction) Money Transfer view """

