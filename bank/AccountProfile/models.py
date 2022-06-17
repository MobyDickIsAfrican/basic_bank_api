import email
from django.db import models
from django.contrib.auth.models import User

class AccountProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False)
    surname = models.CharField(max_length=100, blank=False)
    identity_number = models.CharField(max_length=100, blank=False)
    email = models.CharField(max_length=100, blank=True)
    contact = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return f'{self.name} {self.surname} - {self.pk}'
