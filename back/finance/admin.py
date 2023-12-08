from django.contrib import admin
from .models import *
from import_export import resources
from import_export.admin import ImportExportMixin, ExportActionModelAdmin
from simple_history.admin import SimpleHistoryAdmin


class TransactionInline(admin.StackedInline):
    model = Transaction
    extra = 0  # Отключает автоматическое создание пустых форм

class CustomHistoryAdmin(SimpleHistoryAdmin, admin.ModelAdmin):    pass


class AccountAdmin(admin.ModelAdmin):
    inlines = [TransactionInline]
    list_display = ['title', 'balance']
    list_filter = ['title']
    readonly_fields = ['balance']
    search_fields = ['title']
    # filter_horizontal = ('title')
    list_display_links = ['title', 'balance']
    # raw_id_fields = ('client')


admin.site.register(Account, AccountAdmin)


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


class TransactionAdmin(CustomHistoryAdmin, ImportExportMixin, ExportActionModelAdmin, admin.ModelAdmin):
    resource_class = TransactionResource
    list_display = ('id', 'user', 'account', 'transaction_type', 'amount', 'date', 'description')
    list_display_links = ('id', 'user', 'account', 'transaction_type', 'amount', 'date', 'description')

    search_fields = ['account__title', 'transaction_type', 'amount', 'description']
    filterset_fields = ['transaction_type', 'amount']
admin.site.register(Transaction, TransactionAdmin)


admin.site.register(IncomeCategory)
admin.site.register(ExpenseCategory)
admin.site.register(Category)

