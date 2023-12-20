from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('get_atm/', views.ATMAPIView.as_view()),
    path('get_currencies/', views.CurrencyAPIView.as_view()),
    path('has_account/', views.HasAccountAPIView.as_view()),
    path('user_info/', views.UserInfoAPIView.as_view()),
    path('get_accounts/', views.AccountInfoAPIView.as_view()),
    path('get_cards/', views.CardInfoAPIView.as_view()),
    path('transfer_money/', views.TransferMoneyAPIView.as_view()),
    path('create_account/', views.CreateAccountAPIView.as_view()),
    path('create_card/', views.CreateCardAPIView.as_view()),
    path('change_status_card/', views.BlockCardAPIView.as_view()),
    path('get_operations/', views.OperationInfoAPIView.as_view()),
]
