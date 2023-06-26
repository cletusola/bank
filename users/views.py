from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
User = get_user_model() 
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
