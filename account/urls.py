from django.urls import path 

from .views import (
    register_account,
    user_info,
    dashboard,
    money_transfer,
    confirm_transaction,
    account_history,
)



urlpatterns = [
    path('join/register/', register_account, name='register'),
    path('join/user_info/', user_info, name="user_info"),
    path('pages/dashboard/', dashboard, name="dashboard"),
    path('transactions/money_transfer/', money_transfer, name='money_transfer'),
    path('transactions/confirm_transaction/', confirm_transaction, name="confirm_transaction"),
    path('transactions/history/', account_history, name="account_history"),
]
