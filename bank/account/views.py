from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import SavingsAccountSerializer, CreditAccountSerializer
from .models import SavingsAccount, CreditAccount, Transaction, Account
from .custom_errors import LimitExceeded
from rest_framework import status
import csv
from django.shortcuts import render
from django.http import HttpResponse
from AccountProfile.models import AccountProfile

class SavingsAccountView(APIView):
    def post(self, request):
        data = request.data
        account_serializer = SavingsAccountSerializer(data={"profile": data.get("profile"),\
                 "type": "S", "amount": data.get("amount")})
        if account_serializer.is_valid():
            try:
                account_serializer.save()
            except Exception as e:
                return Response(data={"error": "please enter the initial amount"},\
                     status=status.HTTP_400_BAD_REQUEST)
            return Response(data=account_serializer.initial_data)
        else:
            return Response(data={"error": account_serializer.errors}, \
                status=status.HTTP_400_BAD_REQUEST)

class CreditAccountView(APIView):
    def post(self, request):
        data = request.data
        account_serializer = CreditAccountSerializer(data={"profile": data.get("profile"),\
                 "type": "C", "amount": data.get("amount")})
        if account_serializer.is_valid():
            try:
                account_serializer.save()
            except Exception as e:
                print(e)
                return Response(data={"error": "please enter the initial amount"}, \
                    status=status.HTTP_400_BAD_REQUEST)
            return Response(data=account_serializer.initial_data)
        else:
            return Response(data={"error": account_serializer.errors}, \
                status=status.HTTP_400_BAD_REQUEST)


class Transact(APIView):
    def post(self, request):
        data = request.data
        if data.get("amount") is None:
            print(data)
            print("nope")
            return Response(data={"error": "please enter a valid amount"}, \
                        status=status.HTTP_400_BAD_REQUEST)
        try:
            if data.get("type") == "savings":
                try:
                    savings = SavingsAccount.objects.get(pk=data.get("from_account"))
                except SavingsAccount.DoesNotExist:
                    return Response(data={"error": "please enter a valid account primary key"}, \
                        status=status.HTTP_400_BAD_REQUEST)
                print("as thought")
                savings.transact(data.get("action"), data.get("amount"))
            elif data.get("type") == "credit":
                try:
                    credit = CreditAccount.objects.get(pk=data.get("from_account"))

                except CreditAccount.DoesNotExist:
                    return Response(data={"error": "please enter a valid account primary key"}, \
                        status=status.HTTP_400_BAD_REQUEST)
                credit.transact(data.get("action"), data.get("amount"))
            elif data.get("type") is None:
                return Response(data={"please specify the account type"}, status=status.HTTP_400_BAD_REQUEST)
        
        except LimitExceeded as e:
            print("cant be")
            return Response(data={"error": e.message}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(data={"transaction": "completed"}, status=status.HTTP_201_CREATED)
        

def report(request):
    response = HttpResponse('text/csv')
    response['Content-Disposition'] = 'attachment; filename=report.csv'
    users = AccountProfile.objects.all()

    writer = csv.writer(response)
    writer.writerow([])

    for user in users:
        writer.writerow([])
        writer.writerow(['---Accounts---'])
        accounts = Account.objects.filter(profile=user.pk)
        writer.writerow(['User', 'pk', 'Type', 'Amount'])

        trans_array = []
        for account in accounts:
            writer.writerow([account.profile,account.pk, account.type, account.amount])
            transactions = Transaction.objects.filter(from_account=account.pk)
            for trans in transactions:
                trans_array.append(trans)
        
        writer.writerow([])
        writer.writerow([])
        
        writer.writerow(['---Transactions---'])
        writer.writerow(['pk', 'Account', 'Action', 'amount'])

        for transaction in trans_array:
            writer.writerow([transaction.pk, transaction.from_account, transaction.action, transaction.amount])

    return response
