from django.urls import path 

from .views import (
    register_account,
    user_info,
    dashboard
)



urlpatterns = [
    path('join/register/', register_account, name='register'),
    path('join/user_info/', user_info, name="user_info"),
    path('pages/dashboard/', dashboard, name="dashboard"),
]
