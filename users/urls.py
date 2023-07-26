from django.urls import path 

from .views import (
    login_request,
    logout_request,
    change_password,
)


urlpatterns = [
    path('join/login/', login_request, name="login"),
    path('join/logout/', logout_request, name="logout"),
    path('pages/change_password', change_password, name="change_password"),
]
