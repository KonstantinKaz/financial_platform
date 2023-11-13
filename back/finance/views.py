from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.db.models import Q

from .models import *
from .permissions import IsAdminOrReadOnly
from .serializers import *
#
#
# class AccountAPIListPagination(PageNumberPagination):
#     page_size = 3
#     page_size_query_param = 'page_size'
#     max_page_size = 2
#
#
# class AccountAPIList(generics.ListCreateAPIView):
#     queryset = Account.objects.all()
#     serializer_class = AccountSerializer
#     permission_classes = (IsAuthenticatedOrReadOnly, )
#     pagination_class = AccountAPIListPagination
#
#
# class AccountAPIUpdate(generics.RetrieveUpdateAPIView):
#     queryset = Account.objects.all()
#     serializer_class = AccountSerializer
#     permission_classes = (IsAuthenticated, )
#
#
# class AccountAPIDestroy(generics.RetrieveDestroyAPIView):
#     queryset = Account.objects.all()
#     serializer_class = AccountSerializer
#     permission_classes = (IsAdminOrReadOnly, )
#
#
#
#
#
# class TransactionAPIListPagination(PageNumberPagination):
#     page_size = 3
#     page_size_query_param = 'page_size'
#     max_page_size = 2
#
# class TransactionAPIList(generics.ListCreateAPIView):
#     serializer_class = TransactionSerializer
#     permission_classes = (IsAuthenticatedOrReadOnly,)
#     pagination_class = TransactionAPIListPagination
#
#
#     def get_non_income_and_transfer_transactions(self):
#         id = self.request.user.id
#         return Transaction.objects.filter(
#             (Q(user_id=id) & ~Q(transaction_type__in=['Доход', 'Перевод'])) | Q(user_id=id, transaction_type='Перевод')
#         )
#
#     def get_salary_and_business_income(self):
#         id = self.request.user.id
#         return Transaction.objects.filter(
#             (Q(user_id=id) & ~Q(transaction_type__in=['Перевод', 'Расход']) & Q(transaction_type='Зарплата')) |
#             (Q(user_id=id) & ~Q(transaction_type__in=['Перевод', 'Расход']) & Q(transaction_type='ИП'))
#         )
#
#
#     def get_queryset(self):
#         id = self.request.user.id
#         query_param_non_income_and_transfer = self.request.query_params.get('non_income_and_transfer', None)
#         query_param_salary_and_business_income = self.request.query_params.get('salary_and_business_income', None)
#
#         if query_param_non_income_and_transfer:
#             return self.get_non_income_and_transfer_transactions()
#
#         if query_param_salary_and_business_income:
#             return self.get_salary_and_business_income()
#
#         return Transaction.objects.all()
#
#
#
# class TransactionAPIUpdate(generics.RetrieveUpdateAPIView):
#     queryset = Transaction.objects.all()
#     serializer_class = TransactionSerializer
#     permission_classes = (IsAuthenticated, )
#
#
# class TransactionAPIDestroy(generics.RetrieveDestroyAPIView):
#     queryset = Transaction.objects.all()
#     serializer_class = TransactionSerializer
#     permission_classes = (IsAdminOrReadOnly, )
#
#






class AccountAPIListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 2


class AccountAPIList(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    pagination_class = AccountAPIListPagination


class AccountAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (IsAuthenticated, )


class AccountAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (IsAdminOrReadOnly, )


class TransactionAPIListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 2


class TransactionAPIList(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = TransactionAPIListPagination

    def get_non_income_and_transfer_transactions(self):
        id = self.request.user.id
        if id is not None:
            return Transaction.objects.filter(
                (Q(user_id=id) & ~Q(transaction_type__in=['Доход', 'Перевод'])) | Q(user_id=id, transaction_type='Перевод')
            )
        return Transaction.objects.none()

    def get_salary_and_business_income(self):
        id = self.request.user.id
        if id is not None:
            return Transaction.objects.filter(
                (Q(user_id=id) & ~Q(transaction_type__in=['Перевод', 'Расход']) &
                 Q(income_category__title='Зарплата')) |
                (Q(user_id=id) & ~Q(transaction_type__in=['Перевод', 'Расход']) &
                 Q(income_category__title='ИП'))
            )
        return Transaction.objects.none()

    def get_queryset(self):
        id = self.request.user.id
        query_param_non_income_and_transfer = self.request.query_params.get('non_income_and_transfer', None)
        query_param_salary_and_business_income = self.request.query_params.get('salary_and_business_income', None)

        if query_param_non_income_and_transfer and id is not None:
            return self.get_non_income_and_transfer_transactions()

        if query_param_salary_and_business_income and id is not None:
            return self.get_salary_and_business_income()

        return Transaction.objects.all()

    # http://127.0.0.1:8000/api/transactions/?salary_and_business_income=true
    # http://127.0.0.1:8000/api/transactions/?non_income_and_transfer=true


class TransactionAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = (IsAuthenticated, )


class TransactionAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = (IsAdminOrReadOnly, )
