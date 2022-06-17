from django.urls import path
from .views import SavingsTransact

urlpatterns = [
    path('savings/', SavingsTransact.as_view()),
]