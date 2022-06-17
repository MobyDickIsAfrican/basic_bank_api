from rest_framework import serializers
from .models import AccountProfile

class AccountProfileSerielizer(serializers.ModelSerializer):
    class Meta:
        model = AccountProfile
        fields = ['user', 'name', 'surname', 'identity_number', 'email', 'contact']
