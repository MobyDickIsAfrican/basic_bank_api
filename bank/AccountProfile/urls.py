
from django.urls import path
from .views import UserView, AccountSummary

urlpatterns = [
    path('profile', UserView.as_view(), name="profile"),
    path('summary/<int:pk>/', AccountSummary.as_view(), name="account-summary")
]
