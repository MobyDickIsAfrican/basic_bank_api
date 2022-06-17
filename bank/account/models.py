from msilib.schema import Error
import profile
from turtle import width
from unicodedata import decimal
from django.db import models
from AccountProfile.models import AccountProfile
from django.utils import timezone
from decimal import Decimal
from .custom_errors import LimitExceeded
#from Transaction.serializers import TransactionSerializer

# Create your models here.
class Account(models.Model):

    TYPES = (("S", "savings"), ("C", "credit"))
    profile = models.ForeignKey(AccountProfile, on_delete=models.CASCADE, default=None,\
         related_name="accounts")
    type = models.CharField(max_length=50, choices=TYPES, blank=False)
    amount = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    def __str__(self):
        return f'{str(self.profile)}'

    def save(self, *args, **kwargs):
        print(f"u oh: {self.amount}")

        # if this is the first time
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()

        print("running")

        return super().save(*args, **kwargs)  



class SavingsAccount(Account):
    LIMIT = 50
    limit = models.DecimalField(default=LIMIT, editable=False, max_digits=7, decimal_places=2)

    # only user of account can withdraw from account
    def withdraw(self, amount):  
        self.amount = self.amount - Decimal(amount)
        try:
            withdrawal = Transaction(from_account=self, action="W", amount=amount)
        except Exception as e:
            print(e)
        
        return self.save(_transaction=withdrawal)

    # anyone can deposit into account

    def save(self, *args, **kwargs):
        if self.amount < self.limit:
            print(self.limit)
            raise LimitExceeded(self.limit)

        
        # if no transaction is being processed
        if "_transaction" not in kwargs:
            return super().save(*args, **kwargs)

        # item should not be passed to parent save kwargs
        kwargs.pop("_transaction")
        print(f"stil: {self.amount}")

        return super().save(*args, **kwargs)

    # anyone can deposit into account
    def deposit(self, amount):
        self.amount = self.amount + Decimal(amount)
        deposit = Transaction(from_account=self, action="D", \
             amount=amount)
        return self.save(_transaction=deposit)
    
    def transact(self, action, amount):
        if action == "D":
            return self.deposit(amount=amount)
        elif action == "W":
            return self.withdraw(amount=amount)

class CreditAccount(Account):
    LIMIT = -20000
    limit = models.DecimalField(default=LIMIT, editable=False, max_digits=7, decimal_places=2)

    # only user of account can withdraw from account
    def withdraw(self, amount):  
        self.amount = self.amount - Decimal(amount)
        try:
            withdrawal = Transaction(from_account=self, action="W", amount=amount)
        except Exception as e:
            print(e)
        
        return self.save(_transaction=withdrawal)
    
    def save(self, *args, **kwargs):
        if self.amount < self.limit:
            raise LimitExceeded(self.limit)
        
        # if no transaction is being processed
        if "_transaction" not in kwargs:
            return super().save(*args, **kwargs)

        transaction = kwargs["_transaction"]
        
        transaction.save()

        # item should not be passed to parent save kwargs
        kwargs.pop("_transaction")

        return super().save(*args, **kwargs)

    # anyone can deposit into account
    def deposit(self, amount):
        self.amount = self.amount + Decimal(amount)
        deposit = Transaction(from_account=self, action="D", \
             amount=amount)
        return self.save(_transaction=deposit)
    
    def transact(self, action, amount):
        if action == "W":
            return self.withdraw(amount=amount)
        elif action == "D":
            return self.deposit(amount=amount)

class Transaction(models.Model): 

    ACTIONS = (("D", "deposit"), ("W", "withdraw"))
    from_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="transactions")
    action = models.CharField(max_length=200, choices=ACTIONS, blank=False)
    amount = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)
    
    def get_data(self):
        return {"pk": self.pk, "from": self.from_account.pk, "action": self.action, \
            "amount": self.amount, "date": self.created_at}
    
    class Meta:
        ordering = ["-pk"]