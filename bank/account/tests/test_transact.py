from django.test import TestCase, Client
from AccountProfile.models import AccountProfile
from django.urls import reverse
from django.contrib.auth.models import User
from account.models import SavingsAccount, CreditAccount

class TransactTest(TestCase):
    def setUp(self):
        user = User.objects.create(username="luvo@k.com", password="password")
        self.profile = AccountProfile(user=user, name="luvo", surname="dlulisa", \
            identity_number="908327", email="luvo@k.com", contact="098766")
        self.profile.save()

        savings = SavingsAccount(profile=self.profile, type="S", amount=100)
        self.savings = savings
        self.savings.save()

        credit = CreditAccount(profile=self.profile, type="C", amount=100)
        self.credit = credit
        self.credit.save()

    def test_no_amount_given_for_savings(self):
        client = Client()
        data = {"from_account": self.savings.pk, "action": "W", "type": "savings"}
        response = client.post(reverse("transact"), data)
        self.assertEqual(400, response.status_code)

    def test_limit_exceeded_for_savings(self):
        client = Client()
        data = {"from_account": self.savings.pk, "action": "W", "amount": 100, "type": "savings"}
        response = client.post(reverse("transact"), data)
        self.assertEqual(400, response.status_code)
    
    def test_limit_not_exceeded_for_savings(self):
        client = Client()
        data = {"from_account": self.savings.pk, "action": "W", "amount": 20, "type": "savings"}
        response = client.post(reverse("transact"), data)
        self.assertEqual(201, response.status_code)
    
    def test_no_amount_given_for_credit(self):
        client = Client()
        data = {"from_account": self.credit.pk, "action": "W", "type": "credit"}
        response = client.post(reverse("transact"), data)
        self.assertEqual(400, response.status_code)

    def test_limit_exceeded_for_credit(self):
        client = Client()
        data = {"from_account": self.credit.pk, "action": "W", "amount": 25000, "type": "credit"}
        response = client.post(reverse("transact"), data)
        self.assertEqual(400, response.status_code)
    
    def test_limit_not_exceeded_for_credit(self):
        client = Client()
        data = {"from_account": self.credit.pk, "action": "W", "amount": 20, "type": "credit"}
        response = client.post(reverse("transact"), data)
        self.assertEqual(201, response.status_code)