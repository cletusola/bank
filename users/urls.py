from django.urls import path 

from .views import (
    login_request,
    logout_request
)


urlpatterns = [
    path('join/login/', login_request, name="login"),
    path('join/logout/', logout_request, name="logout"),
]
