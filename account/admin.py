from django.contrib import admin

from .models import Account, Account_History



# customer admin
# class CustomerAdmin(admin.ModelAdmin):
#     list_display = ['first_name','last_name','username','email','date']
#     list_display_links = ['first_name','last_name','username','email']
#     list_filter = ['date']

# admin.site.register(Customer, CustomerAdmin)


# account admin 
class AccountAdmin(admin.ModelAdmin):
    list_display = ['account_number','account_owner','date_opened']
    list_display_links = ['account_number','account_owner','date_opened']

admin.site.register(Account, AccountAdmin)


# account history admin
class AccountHistoryAdmin(admin.ModelAdmin):
    list_display = ['sender_account', 'reciever_account','transaction_type']
    list_display_links = ['sender_account', 'reciever_account','transaction_type']

admin.site.register(Account_History, AccountHistoryAdmin)