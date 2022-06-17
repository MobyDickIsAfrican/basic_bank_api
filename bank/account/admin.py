from django.contrib import admin
from .models import Account, SavingsAccount, CreditAccount, Transaction

admin.site.register(Account)
admin.site.register(SavingsAccount)
admin.site.register(CreditAccount)
admin.site.register(Transaction)

# Register your models here.
