from django.db import models
#from account.models import Account

# Create your models here.
class Transaction(models.Model): 

    ACTIONS = (("D", "deposit"), ("W", "withdraw"))
    from_account = models.ForeignKey("account.Account", on_delete=models.SET_NULL, default=None, null=True)
    action = models.CharField(max_length=200, choices=ACTIONS, blank=False)
    amount = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)