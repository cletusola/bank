from django.contrib import admin

from .models import Account, Account_History



# account admin 
class AccountAdmin(admin.ModelAdmin):
    list_display = ['account_name','account_number','account_owner','date_opened']
    list_display_links = ['account_name','account_number','account_owner','date_opened']

admin.site.register(Account, AccountAdmin)


# account history admin
class AccountHistoryAdmin(admin.ModelAdmin):
    list_display = ['account_history_owner','sender_name', 'reciever_account','reciever_account_name','transaction_type','time']
    list_display_links = ['account_history_owner','sender_name', 'reciever_account','reciever_account_name','transaction_type']

admin.site.register(Account_History, AccountHistoryAdmin)