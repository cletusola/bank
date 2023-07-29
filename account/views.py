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
    TransferForm,
    ChangePinForm,
    UserInfoForm,
    ProfileInfoForm,
)

from .models import (
    Account,
    Account_History
)

import random 
import time
import io 


# function to generate account number 
def generate_account_number():

    gen_rand = random.randrange(0000000, 9999999, 7)
    account_identifier = 23 

    account_number_string = str(account_identifier) + str(gen_rand)
    account_number_int = int(account_number_string)

    return account_number_int


# create account history 
def create_account_history(history_owner, sender_name, reciever, reciever_name, amount, bal_bf, bal_aft):
    history = Account_History.objects.create(
        account_history_owner = history_owner,
        sender_name = sender_name,
        reciever_account = reciever,
        reciever_account_name = reciever_name,
        transaction_type = "money transfer",
        amount = amount,
        balance_before_transaction = bal_bf,
        balance_after_transaction = bal_aft
    )

    history.save()



# home view 
def home(request):
    return render(request, "pages/home.html")

""" Account opening and registration view """

# account info view
def register_account(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == "POST":
        form = AccountInformationForm(request.POST)
        if form.is_valid():
            request.session['first_name'] = form.cleaned_data['first_name']
            request.session['last_name'] = form.cleaned_data['last_name']
            request.session['phone'] = form.cleaned_data['phone']
            request.session['address'] = form.cleaned_data['address']
            request.session['occupation'] = form.cleaned_data['occupation']
            request.session['account_type'] = form.cleaned_data['account_type']

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
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password2']
            transaction_pin = form.cleaned_data['transaction_pin']

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
                    account_name = user.first_name + " " + user.last_name,
                    account_number = generate_account_number(),
                    account_owner = user,
                    account_type = request.session['account_type'],
                    account_address = request.session['address'],
                    account_phone = request.session['phone'],
                    account_occupation = request.session['occupation'],
                    transaction_pin = transaction_pin
                )
                account.save()
                messages.success(request, "Account created ")
                login(request, user)
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
    profile =  Account.objects.filter(account_owner=request.user)
    return render(request, 'pages/dashboard.html', context={'profile':profile})

""" Account view ends"""

 

""" (Transaction) Money Transfer view """
# transfer view 
@login_required(login_url='login')
def money_transfer(request):
    if request.method == "POST":
        form = TransferForm(request.POST)
        if form.is_valid():
            reciever_account = form.cleaned_data['account']
            amount = form.cleaned_data['amount']
            request.session['reciever_account'] = reciever_account
            request.session['amount'] = amount

            # check if account exist
            chk_account =  Account.objects.filter(account_number=reciever_account)
            for a in chk_account:
                account_name = a.account_name
            
            if chk_account.count():
                reciever_name = account_name
                request.session['reciever_name'] = reciever_name

            # fetch sender account balance
            user_account = Account.objects.filter(account_owner=request.user)
            
            for u in user_account:
                account_balance = int(u.account_balance)

                # print(type(amount))
                # int_amount = int(amount)
                # print(type(int_amount))

            if chk_account.count() and account_balance >= int(amount):

                return redirect("confirm_transaction")
            
            # if account does not exist
            if not chk_account.count():
                messages.error(request, "Unable to find user with this account")
                return render(request, "transactions/money_transfer.html", {"form":form})
            
            # if amount is greater than user account balance 
            if amount > account_balance:
                messages.error(request, "You do not have enough money in your account")
                return render(request, "transactions/money_transfer.html", {"form":form})
        
        else:
            messages.error(request, "Please provide the required details to continue with your transaction")
            return render(request, "transactions/money_transfer.html", {"form":form})
        
    else:
        form = TransferForm()
        account = Account.objects.filter(account_owner=request.user)

        return render(request, "transactions/money_transfer.html", {"form":form,"account":account})

    
# confirm transaction 
@login_required(login_url='login')
def confirm_transaction(request):
    if request.method == "POST":
        reciever_account = request.session['reciever_account']
        amount = int(request.session['amount'])
        reciever_name = request.session['reciever_name']

        try:
            # fetch sender account 
            sender = Account.objects.get(account_owner=request.user)
            # sender account name 
            sender_name = sender.account_name
            # sender bal before transaction 
            sender_bal_before_transaction = sender.account_balance
            #deduct amount from sender bal 
            new_sender_balance = int(sender.account_balance) - int(amount)
            #sender new balance
            sender.account_balance = new_sender_balance
            sender.save()
            # sender bal after transaction 
            sender_bal_after_transaction = sender.account_balance 
            
            #fetch receiver account
            reciever = Account.objects.get(account_number=reciever_account)
            #reciever name 
            reciever_account_name = reciever.account_name
            # reciever bal before transaction 
            reciever_bal_before_transaction = reciever.account_balance
            # add amount to receiver bal 
            new_reciever_balance = int(reciever.account_balance) + int(amount)
            # reciever new balance
            reciever.account_balance = new_reciever_balance
            reciever.save()
            # reciever bal after transaction 
            reciever_bal_after_transaction = reciever.account_balance

            try:
                sender_history = create_account_history (
                    sender,
                    sender_name,
                    reciever,
                    reciever_account_name,
                    amount,
                    sender_bal_before_transaction,
                    sender_bal_after_transaction
                )

                reciever_history = create_account_history (
                    reciever,
                    sender_name,
                    reciever,
                    reciever_account_name,
                    amount,
                    reciever_bal_before_transaction,
                    reciever_bal_after_transaction
                )

                messages.success(request, "Transfer successful")
                return redirect("dashboard")
            
            except:
                messages.info(request, "Transfer successful, but could not create transaction history")           
                return redirect("dashboard")
        
        except:
            messages.error(request, "Unable to perform transaction, please try again later")
            return render(request, "transactions/confirm_transaction.html")
    
    else:
        reciever_account = request.session['reciever_account']
        amount = request.session['amount']
        reciever_name = request.session['reciever_name']

        context = {
            "reciever_account":reciever_account,
            "reciever_name":reciever_name,
            "amount":amount
        }

        return render(request, "transactions/confirm_transaction.html", context=context)

""" (Transaction) Money Transfer view """

# transaction history 
@login_required(login_url="login")
def account_history(request):
    account = Account.objects.filter(account_owner=request.user)
    for a in account:
        account_number = a.account_number
    history = Account_History.objects.filter(account_history_owner=account_number)
    return render(request, "transactions/account_history.html", {"history":history})


# change transaction pin 
@login_required(login_url="login")
def change_pin(request):
    if request.method == "POST":
        form = ChangePinForm(request.POST)

        if form.is_valid():
            pin = form.cleaned_data["pin2"]

            # get user account
            account = Account.objects.get(account_owner=request.user)
            account.transaction_pin = pin 
            account.save()

            messages.success(request, "Transaction pin changed successfully")
            return redirect("dashboard")
        
        else:
            messages.error(request, "please provide valid inputs")
            return render(request, "pages/change_pin.html", {"form":form})
    
    else:
        form = ChangePinForm()
        return render(request, "pages/change_pin.html", {"form":form})
    

# update user and profile information 
@login_required(login_url="login")
def update_info(request):
    user_profile = Account.objects.get(account_owner=request.user)
    if request.method == "POST":
        
        user_form = UserInfoForm(request.POST, instance=request.user)
        profile_form = ProfileInfoForm(request.POST, instance=user_profile)

        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "information updated successfully")
            return redirect("dashboard")
        
        else:
            messages.error(request,"please provide valid informations")
            return render(request, "pages/update_form.html",{"user_form":user_form,
                                                             "profile_form":profile_form
                                                             })
    
    else:
        user_form = UserInfoForm(instance=request.user)
        profile_form = ProfileInfoForm(instance=user_profile)
        return render(request, "pages/update_form.html",{"user_form":user_form,
                                                         "profile_form":profile_form
                                                         })