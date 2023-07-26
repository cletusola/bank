from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
User = get_user_model() 
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages 
from django.contrib.auth.decorators import login_required


from .forms import (
    LogInForm,
    ChangePassword
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
    

""" change password view """
@login_required(login_url="login")
def change_password(request):
    if request.method == "POST":
        form = ChangePassword(request.POST)

        if form.is_valid():
            user = request.user 
            current_password = form.cleaned_data["current_password"]
            new_password = form.cleaned_data["new_password_again"]
            user_password = user.password 

            print(user.password)
            print(new_password)
            if current_password != user_password:
                messages.error(request, "Current password is incorrect")
                
            elif current_password == new_password:
                messages.error(request, "You can not use the same password as your old password")
            
            else:
                pass 

            user.set_password(new_password)
            messages.success(request, "You have successfully changed your password")
            return redirect("dashboard")
        
        else:
            messages.error(request, "please provide valid informations")
            return render(request, "pages/change_password.html", {"form":form})
    
    else:
        form = ChangePassword()
        return render(request, "pages/change_password.html", {"form":form}) 