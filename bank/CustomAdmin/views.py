from django.shortcuts import render
from AccountProfile.models import AccountProfile
from account.models import Account, Transaction
from rest_framework import status
from django.http import HttpResponseBadRequest

def admin(request, pk):
    try:
        user = AccountProfile.objects.get(id=pk)
    except AccountProfile.DoesNotExist:
        print("running")
        return HttpResponseBadRequest("user does not exist")

    trans_array = []
    accounts = Account.objects.filter(profile=user.id)
    for account in accounts:
        transactions = Transaction.objects.filter(from_account=account.pk)
        for trans in transactions:
            trans_array.append(trans)
 
    context = {
        'user' : user,
        'accounts': accounts,
        'transactions' : trans_array
    }
    print("going once")
    return render(request, 'CustomAdmin/admin.html', context)