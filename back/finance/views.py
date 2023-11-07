from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.db.models import Q

from .models import *
from .permissions import IsAdminOrReadOnly
from .serializers import FinanceSerializer


class AccountAPIListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 2


class AccountAPIList(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = FinanceSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    pagination_class = AccountAPIListPagination


class AccountAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Account.objects.all()
    serializer_class = FinanceSerializer
    permission_classes = (IsAuthenticated, )


class AccountAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = FinanceSerializer
    permission_classes = (IsAdminOrReadOnly, )





class TransactionAPIList(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = FinanceSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    pagination_class = AccountAPIListPagination

    # def get_queryset(self):
    #     # Пример фильтрации с использованием Q и логических операторов
    #     return Transaction.objects.filter(
    #         Q(transaction_type='Доход') | Q(transaction_type='Перевод'),
    #         amount__gt=100
    #     )


class TransactionAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = FinanceSerializer
    permission_classes = (IsAuthenticated, )


class TransactionAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = FinanceSerializer
    permission_classes = (IsAdminOrReadOnly, )