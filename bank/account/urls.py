from django.contrib import admin
from django.urls import path
from .views import SavingsAccountView, CreditAccountView, Transact, report

urlpatterns = [
    path('savings', SavingsAccountView.as_view(), name="savings"),
    path('credit', CreditAccountView.as_view(), name="credit"),
    path('transact', Transact.as_view(), name="transact"),
    path('report', report, name="report")
]
