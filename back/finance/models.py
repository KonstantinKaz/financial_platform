from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from simple_history.models import HistoricalRecords


class Category(models.Model):
    CATEGORY_TYPES = (
        ('income', 'Доход'),
        ('expense', 'Расход'),
        ('transfer', 'Перевод'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=CATEGORY_TYPES, null=True, blank=True)

    def __str__(self):
        return self.title

class IncomeCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class ExpenseCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Установите значение по умолчанию 0

    def __str__(self):
        return self.title

    def update_balance(self):
        income = self.transaction_set.filter(transaction_type='Доход').aggregate(Sum('amount'))['amount__sum'] or 0
        expenses = self.transaction_set.filter(transaction_type__in=['Расход', 'Перевод']).aggregate(Sum('amount'))[
                       'amount__sum'] or 0

        self.balance = income - expenses

        self.save()



class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('Доход', 'Доход'),
        ('Расход', 'Расход'),
        ('Перевод', 'Перевод'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    income_category = models.ForeignKey(IncomeCategory, on_delete=models.SET_NULL, null=True, blank=True)
    expense_category = models.ForeignKey(ExpenseCategory, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    history = HistoricalRecords(inherit=True)
    # history = HistoricalRecords(
        # fields=['transaction_type', 'amount', 'income_category', 'expense_category', 'date', 'description'])

    def __str__(self):
        return f"Транзакция {self.id} от {self.user}: {self.amount} ({self.transaction_type})"

    def save(self, *args, **kwargs):
        # Вызовите метод update_balance у связанного счета при сохранении транзакции
        super().save(*args, **kwargs)
        self.account.update_balance()




