from django.db import IntegrityError
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.contrib.auth.models import User
from AccountProfile.models import AccountProfile
from .serializers import AccountProfileSerielizer
from account.models import CreditAccount, SavingsAccount

class UserView(APIView):
    def post(self, request, format='json'):
        data = request.data
        try:
            user = User.objects.create(username=data.get("email"), password=data.get("password"))
        except IntegrityError:
            return Response(data={"error": "please enter valid email and password"})
            
        user_serializer = AccountProfileSerielizer(data={"user": user.pk, \
             "name": data.get("name"), "surname": data.get("surname"),\
                 "identity_number": data.get("identity_number"), \
                "email": data.get("email"), "contact": data.get("contact")})
        if user_serializer.is_valid():
            user_serializer.save()
        else:
            user.delete()
            return Response(data={"error": user_serializer.errors})
        
        return Response(data=user_serializer.initial_data, status=status.HTTP_201_CREATED)

class AccountSummary(APIView):

    def get(self, request, pk):
        try:
            user_profile = AccountProfile.objects.get(pk=pk)
        except AccountProfile.DoesNotExist:
            return Response(data={"error": "account matching query not found"},\
                 status=status.HTTP_404_NOT_FOUND)
        
        #get all accounts belonging to user
        accounts = user_profile.accounts.all()
        credit_or_savings = {"credit": [], "savings": []}
        for account in accounts:
            '''
            store last 10 transactions in dict in the form {"pk": "", "type": "", "amount": "",
             "transactions": [trans]}
            '''
            account_obj = {}
            last_transactions = account.transactions.all()[:10]
            transactions_array = []

            for trans in last_transactions:
                transactions_array.append(trans.get_data())
            
            account_obj["pk"] = account.pk
            account_obj["amount"] = account.amount
            account_obj["transactions"] = transactions_array

            if account.type == "S":
                credit_or_savings["savings"].append(account_obj)

            elif account.type == "C":
                credit_or_savings["credit"].append(account_obj)
        
        return Response(data=credit_or_savings, status=status.HTTP_200_OK)

            
