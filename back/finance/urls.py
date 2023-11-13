from django.contrib import admin
from django.urls import path

from .views import *

urlpatterns = [
    path('accounts/', AccountAPIList.as_view()),
    path('accounts/<int:pk>/', AccountAPIUpdate.as_view()),
    path('accounts/delete/<int:pk>/', AccountAPIDestroy.as_view()),  # Измененный путь для удаления счетов

    path('transactions/', TransactionAPIList.as_view()),
    path('transactions/<int:pk>/', TransactionAPIUpdate.as_view()),
    path('transactions/delete/<int:pk>/', TransactionAPIDestroy.as_view()),  # Измененный путь для удаления транзакций
]
