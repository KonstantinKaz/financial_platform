from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import *
from .permissions import IsAdminOrReadOnly
from .serializers import *


class AccountAPIListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 2

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    pagination_class = AccountAPIListPagination


class TransactionAPIListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 2

class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = TransactionAPIListPagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]  # Add DjangoFilterBackend
    search_fields = ['transaction_type', 'amount', 'description', 'income_category__title', 'expense_category__title']
    filterset_fields = ['transaction_type', 'amount', 'income_category__title', 'expense_category__title']

    @action(detail=False, methods=['GET'])
    def non_income_and_transfer(self, request):
        id = self.request.user.id
        if id is not None:
            transactions = Transaction.objects.filter(
                (Q(user_id=id) & ~Q(transaction_type__in=['Доход', 'Перевод'])) | Q(user_id=id,
                                                                                    transaction_type='Перевод')
            )
            serializer = self.get_serializer(transactions, many=True)
            return Response(serializer.data)
        return Response([])

    @action(detail=False, methods=['GET'])
    def salary_and_business_income(self, request):
        id = self.request.user.id
        if id is not None:
            transactions = Transaction.objects.filter(
                (Q(user_id=id) & ~Q(transaction_type__in=['Перевод', 'Расход']) &
                 Q(income_category__title='Зарплата')) |
                (Q(user_id=id) & ~Q(transaction_type__in=['Перевод', 'Расход']) &
                 Q(income_category__title='ИП'))
            )
            serializer = self.get_serializer(transactions, many=True)
            return Response(serializer.data)
        return Response([])


    def get_queryset(self):
        id = self.request.user.id
        query_param_non_income_and_transfer = self.request.query_params.get('non_income_and_transfer', None)
        query_param_salary_and_business_income = self.request.query_params.get('salary_and_business_income', None)

        if query_param_non_income_and_transfer and id is not None:
            return self.get_non_income_and_transfer_transactions()

        if query_param_salary_and_business_income and id is not None:
            return self.get_salary_and_business_income()

        return Transaction.objects.all()


class IncomeCategoryViewSet(viewsets.ModelViewSet):
    queryset = IncomeCategory.objects.all()
    serializer_class = IncomeCategorySerializer

    @action(detail=False, methods=['POST'])
    def create_transaction(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @action(detail=True, methods=['PUT'])
    def update_category(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @action(detail=True, methods=['DELETE'])
    def delete_category(self, request, pk=None):
        instance = self.get_object()
        instance.delete()
        return Response(status=204)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class ExpenseCategoryViewSet(viewsets.ModelViewSet):
    queryset = ExpenseCategory.objects.all()
    serializer_class = ExpenseCategorySerializer