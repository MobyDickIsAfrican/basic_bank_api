from dataclasses import field
from rest_framework import serializers
from .models import SavingsAccount, CreditAccount

class SavingsAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingsAccount
        fields = ['profile', 'type', 'amount', ]

class CreditAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditAccount
        fields = ['profile', 'type', 'amount', ]