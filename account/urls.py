from django.urls import path 
from django.conf import settings 
from django.conf.urls.static import static 

from .views import (
    register_account,
    user_info,
    dashboard,
    money_transfer,
    confirm_transaction,
    change_pin,
    update_info,
)



urlpatterns = [
    path('join/register/', register_account, name='register'),
    path('join/user_info/', user_info, name="user_info"),
    path('pages/dashboard/', dashboard, name="dashboard"),
    path('transactions/money_transfer/', money_transfer, name='money_transfer'),
    path('transactions/confirm_transaction/', confirm_transaction, name="confirm_transaction"),
    path('pages/change_pin/', change_pin, name="change_pin"),
    path('pages/update_info/', update_info, name="update_info")
]
urlpatterns += static(settings.MEDIA_URL,
                            document_root = settings.MEDIA_ROOT)