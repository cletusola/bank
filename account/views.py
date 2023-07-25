from django.shortcuts import render, redirect
from django.http import HttpResponse
# from django.contrib.auth import login, authenticate, logout
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
User = get_user_model()

from .forms import (
    AccountInformationForm,
    UserInformationForm,
    TransferForm,
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


# create account history 
def create_account_history(history_owner, sender, reciever, reciever_name, amount, bal_bf, bal_aft):
    history = Account_History.objects.create(
        account_history_owner = history_owner,
        sender_account = sender,
        reciever_account = reciever,
        reciever_account_name = reciever_name,
        transaction_type = "money transfer",
        amount = amount,
        balance_before_transaction = bal_bf,
        balance_after_transaction = bal_aft
    )

    history.save()

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
    # profile = Account.objects.filter(account_owner=request.user)
    profile = "abc"
    return render(request, 'pages/dashboard.html', context={'profile':profile})

""" Account view ends"""

 

""" (Transaction) Money Transfer view """
# transfer view 
@login_required(login_url='login')
def money_transfer(request):
    if request.method == "POST":
        form = TransferForm(request.POST)
        if form.is_valid():
            reciever_account = form.cleaned_data['receiver_account']
            amount = form.cleaned_data['amount']
            request.session['reciever_account'] = reciever_account
            request.session['amount'] = amount

            # check if account exist
            chk_account = Account.objects.filter(account_number=reciever_account)
            
            if chk_account.count():
                reciever_name = chk_account.account_owner.first_name + " " + chk_account.account_owner.last_name
                request.session['reciever_name'] = reciever_name

            # fetch sender account balance
            user_account = Account.objects.filter(account_owner=request.user)
            user_balance = user_account.account_balance 

            if chk_account.count() and user_balance >= amount:

                return redirect("confirm_transaction")
            
            # if account does not exist
            if not chk_account.count():
                messages.error(request, "Unable to find user with this account")
                return render(request, "transactions/money_transfer.html", {"form":form})
            
            # if amount is greater than user account balance 
            if amount > user_balance:
                messages.error(request, "You do not have enough money in your account")
                return render(request, "transactions/money_transfer.html", {"form":form})
        
        else:
            messages.error(request, "Please provide the required details to continue with yur transaction")
            return render(request, "transactions/money_transfer.html", {"form":form})
        
    else:
        form = TransferForm()
        return render(request, "transactions/money_transfer.html", {"form":form})

    
# confirm transaction 
@login_required(login_url='login')
def confirm_transaction(request):
    if request.method == "POST":
        reciever_account = request.session['reciever_account']
        amount = request.session['amount']
        reciever_name = request.session['reciever_name']

        try:
            # fetch sender account 
            sender = Account.objects.filter(account_owner=request.user)
            # sender account name 
            sender_name = sender.account_owner.first_name + " " + sender.account_owner.last_name
            # sender bal before transaction 
            sender_bal_before_transaction = sender.account_balance
            #deduct amount from sender bal 
            sender.account_balance - amount
            sender.save()
            # sender bal after transaction 
            sender_bal_after_transaction = sender.account_balance 
            
            #fetch receiver account
            reciever = Account.objects.filter(account_number=reciever_account)
            # reciever bal before transaction 
            reciever_bal_before_transaction = reciever.account_balance
            # add amount to receiver bal 
            reciever.account_balance + amount 
            reciever.save()
            # reciever bal after transaction 
            reciever_bal_after_transaction = reciever.account_balance

            try:
                # create transaction history 
                sender_history = create_account_history(
                    sender, 
                    sender_name, 
                    reciever,
                    reciever_name,
                    amount,
                    sender_bal_before_transaction,
                    sender_bal_after_transaction
                    )
                
                receiver_history = create_account_history(
                    reciever,
                    sender_name,
                    reciever,
                    reciever_name,
                    amount,
                    reciever_bal_before_transaction,
                    reciever_bal_after_transaction
                )
            except:
                messages.info(request, "could not create transaction history")

        except:
            messages.error(request, "Unable to perform transaction, please try again later")
            return render(request, "transactions/confrim_transaction.html")
    
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

