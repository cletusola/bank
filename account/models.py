from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
 



# account model 
class Account(models.Model):
    acc_type = (
        ('savings','savings'),
        ('checkings','checkings')
    )
    account_name = models.CharField(max_length=60, null=False, blank=False)
    account_number = models.IntegerField(null=False,blank=False)
    account_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    account_balance = models.IntegerField(default=0.00, null=False,blank=False)
    account_type = models.CharField(choices=acc_type, default='savings', max_length=20, null=False, blank=False)
    account_address = models.CharField(max_length=150, null=False,blank=False)
    account_phone = models.CharField(max_length=14, null=False, blank=False)
    account_occupation = models.CharField(max_length=60, null=False, blank=False)
    transaction_pin = models.IntegerField(null=False, blank=False)
    date_opened = models.DateField(auto_now_add=True)
    time_opened = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-time_opened']

    def __str__(self):
        return f"{self.account_owner.username}"
    
# account history 
class Account_History(models.Model):
    account_history_owner = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="history_owner")
    sender_name= models.CharField(max_length=60, null=False, blank=False)
    reciever_account = models.ForeignKey(Account, on_delete=models.CASCADE,related_name="receiver")
    receiver_account_name = models.CharField(max_length=60, null=False,blank=False)
    transaction_type = models.CharField(max_length=50, null=False,blank=False)
    amount = models.CharField(max_length=30, null=True, blank=True)
    balance_before_transaction = models.IntegerField(null=False,blank=False)
    balance_after_transaction = models.IntegerField(null=False,blank=False)
    date = models.DateField(auto_now_add=True)
    time = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-time']


    def __str__(self):
        return f"{self.sender_account.account_number}"