# from django.contrib import admin
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import *
#
# router = DefaultRouter()
# router.register(r'accounts', AccountAPIList, basename='account')
# router.register(r'transactions', TransactionViewSet, basename='transaction')
#
#
# urlpatterns = [
#     path('accounts/', AccountAPIList.as_view()),
#     path('accounts/<int:pk>/', AccountAPIUpdate.as_view()),
#     path('accounts/delete/<int:pk>/', AccountAPIDestroy.as_view()),  # Измененный путь для удаления счетов
#
#     path('transactions/', TransactionAPIList.as_view()),
#     path('transactions/<int:pk>/', TransactionAPIUpdate.as_view()),
#     path('transactions/delete/<int:pk>/', TransactionAPIDestroy.as_view()),  # Измененный путь для удаления транзакций
# ]

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'accounts', AccountViewSet, basename='account')
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'income-categories', IncomeCategoryViewSet, basename='income-category')
router.register(r'expense-categories', ExpenseCategoryViewSet, basename='expense-category')

urlpatterns = [
    path('', include(router.urls)),
    # other URL patterns
]
