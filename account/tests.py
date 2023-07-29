from django.test import TestCase, Client
from django.urls import reverse 
from django.contrib.auth import get_user_model
User = get_user_model()

from .models import Account, Account_History


# test all tasks
class Test(TestCase):
    #setup 
    def setUp(self):
        self.user = User.objects.create_user(
            first_name="test",
            last_name='user',
            email = "testuser@email.com",
            username = 'testuser',
            password= 'T3stUS3R@@'
        )
        self.user.save()

        self.account1 = Account.objects.create(
            account_name = f"{self.user.first_name} {self.user.last_name}",
            account_number = 238909847,
            account_owner = self.user,
            account_type = "savings",
            account_address = "123 abc st, efg",
            account_phone = "123456789",
            account_occupation = "Teacher",
            transaction_pin = "1111",
            account_balance=200
        )
        self.account1.save()

        self.account2 = Account.objects.create(
            account_name = f"{self.user.first_name} {self.user.last_name}",
            account_number = 238909888,
            account_owner = self.user,
            account_type = "savings",
            account_address = "123 abc st, efg",
            account_phone = "123434567",
            account_occupation = "Teacher",
            transaction_pin = "1111",
        )
        self.account2.save()

    # dashboard test 
    def test_dashboard(self):
        # force login user
        self.client.force_login(self.user)
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
    
    # get request to money transfer page
    def test_get_money_transfer(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("money_transfer"))
        self.assertEqual(response.status_code, 200)


    # post request to money transfer page
    def test_post_money_transfer(self):
        self.client.force_login(self.user)
        payload = {
            "reciever_account":self.account2.account_number,
            "amount":20
        }
        response = self.client.post(reverse("money_transfer"),payload)
        self.assertEqual(response.status_code,200)

    # get request to confirm transaction page
    def test_get_confirm_transaction(self):
        self.client.force_login(self.user)
        session = self.client.session
        session["reciever_account"] = self.account2.account_number
        session["amount"] = "20"
        session["reciever_name"] = self.account2.account_name
        session.save()

        response = self.client.get(reverse("confirm_transaction"))
        self.assertEqual(response.status_code,200)

    # post request to confirm transaction page
    def test_post_confirm_transaction(self):
        self.client.force_login(self.user)
        session = self.client.session
        session["reciever_account"] = self.account2.account_number
        session["amount"] = "20"
        session["reciever_name"] = self.account2.account_name
        session.save()

        response = self.client.post(reverse("confirm_transaction"))
        self.assertEqual(response.status_code,200)


    # test get request for account history 
    def test_get_account_history(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("account_history"))
        self.assertEqual(response.status_code,200)

    # test get request for change transaction pin
    def test_get_change_pin(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("change_pin"))
        self.assertEqual(response.status_code,200)

    # test post request for change transaction pin
    def test_post_change_pin(self):
        self.client.force_login(self.user)
        payload = {
            "pin":"2345"
        }
        response = self.client.post(reverse("change_pin"),payload)
        self.assertEqual(response.status_code,200)


