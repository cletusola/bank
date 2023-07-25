from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
User = get_user_model() 
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages 
from django.contrib.auth.decorators import login_required


from .forms import (
    LogInForm
)


""" authentication view begins """
#login request
def login_request(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    
    if request.method == "POST":
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(username=username, password=password)
            
            if user is not None:
                if user.is_active == True:
                    login(request, user)
                    return redirect("dashboard")
                else:
                    messages.info(request, "Your account is inactive, contact our support for help")
                    return render(request, "join/login.html", {"form":form})
            
            else:
                messages.error(request, "Incorrect username or password")
                return render(request, "join/login.html", {"form":form})
        else:
            messages.error(request, "Please provide a valid input")
            return render(request, "join/login.html", {"form":form})
    else:
        form = LogInForm()
        return render(request, "join/login.html", {"form":form})


# logout request
def logout_request(request):
    logout(request)
    return redirect("home")

""" authentication view ends """     
    