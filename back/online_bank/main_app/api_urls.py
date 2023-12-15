from django.contrib import admin
from django.urls import path, include
from .views import ATMAPIView, CurrencyAPIView, HasAccountAPIView

urlpatterns = [
    path('get_atm/', ATMAPIView.as_view()),
    path('get_currencies/', CurrencyAPIView.as_view()),
    path('has_account/', HasAccountAPIView.as_view()),
]
