from django.urls import path 

from .views import (
    register_account,
    user_info,
    dashboard,
    money_transfer,
    confirm_transaction,
    home,
)



urlpatterns = [
    path('', home, name="home"),
    path('join/register/', register_account, name='register'),
    path('join/user_info/', user_info, name="user_info"),
    path('pages/dashboard/', dashboard, name="dashboard"),
    path('transactions/money_transfer/', money_transfer, name='money_transfer'),
    path('transactions/confirm_transaction/', confirm_transaction, name="confirm_transaction"),
]
