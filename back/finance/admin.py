from django.contrib import admin

from .models import *

# Register your models here.
from django.contrib import admin
from .models import Account, Transaction
# from django.contrib import adminfrom simple_history.admin import SimpleHistoryAdmin
# from simple_history.admin import SimpleHistoryAdmin

from import_export.admin import ImportExportMixin, ExportActionModelAdmin
class TransactionInline(admin.StackedInline):
    model = Transaction
    extra = 0  # Отключает автоматическое создание пустых форм



class AccountAdmin(admin.ModelAdmin):
    inlines = [TransactionInline]  # Добавляет инлайн транзакций к административному классу счета
    list_display = ['title', 'balance']
    list_filter = ['title']
    readonly_fields = ['balance']


admin.site.register(Account, AccountAdmin)

admin.site.register(IncomeCategory)
admin.site.register(ExpenseCategory)

from import_export import resources, fields
from import_export.widgets import DateWidget
from import_export.admin import ExportMixin, ImportExportModelAdmin

class TransactionResource(resources.ModelResource):
    class Meta:
        model = Transaction
        fields = ('id', 'user__username', 'account__title', 'transaction_type', 'amount', 'income_category__title', 'expense_category__title', 'date', 'description')

    # Кастомизация QuerySet для экспорта
    def get_export_queryset(self, request):
        return super().get_export_queryset(request).select_related('user', 'account', 'income_category', 'expense_category')

    # Кастомизация значения поля перед экспортом
    def dehydrate_date(self, transaction):
        return transaction.date.strftime('%Y-%m-%d')  # Пример форматирования даты

    # Кастомизация значения поля при извлечении для экспорта
    def get_income_category(self, transaction):
        return transaction.income_category.title if transaction.income_category else ''

    def get_expense_category(self, transaction):
        return transaction.expense_category.title if transaction.expense_category else ''


class TransactionAdmin(ImportExportMixin, ExportActionModelAdmin, admin.ModelAdmin):
    resource_class = TransactionResource
    list_display = ('id', 'user', 'account', 'transaction_type', 'amount', 'income_category', 'expense_category', 'date', 'description')
    search_fields = ['id', 'user__username', 'account__title']


# class TransactionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
#     resource_class = TransactionResource
#
#     def get_export_queryset(self, request):
#         queryset = super().get_export_queryset(request)
#         if self.model is Transaction:
#             return queryset.select_related('user', 'account', 'income_category', 'expense_category')
#         return queryset


admin.site.register(Transaction, TransactionAdmin)
