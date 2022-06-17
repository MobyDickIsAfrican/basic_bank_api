from django.shortcuts import render
from .models import Transaction
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import TransactionSerializer
from account.models import SavingsAccount


class SavingsTransact(APIView):
    def post(self, request):
        data = request.data
        print(data.get("from_account"))
        savings = SavingsAccount.objects.get(pk=data.get("from_account"))
        savings.transact(data.get("action"), data.get("amount"))
        
        return Response(data={"transaction": "completed"})
            
            

