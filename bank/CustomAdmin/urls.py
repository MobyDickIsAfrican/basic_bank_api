from django.contrib import admin
from django.urls import path
from .views import admin

urlpatterns = [
    path('<int:pk>', admin, name="custom-admin"),
]