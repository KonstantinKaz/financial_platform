from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Установите значение по умолчанию 0

    def __str__(self):
        return self.title

    def update_balance(self):
        # Вычислите сумму всех доходов и расходов
        income = self.transaction_set.filter(transaction_type='Доход').aggregate(Sum('amount'))['amount__sum'] or 0
        expenses = self.transaction_set.filter(transaction_type='Расход').aggregate(Sum('amount'))['amount__sum'] or 0

        # Обновите баланс
        self.balance = income - expenses

        # Сохраните изменения
        self.save()

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('Доход', 'Доход'),
        ('Расход', 'Расход'),
        ('Перевод', 'Перевод'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"Транзакция {self.id} от {self.user}: {self.amount} ({self.transaction_type})"

    def save(self, *args, **kwargs):
        # Вызовите метод update_balance у связанного счета при сохранении транзакции
        super().save(*args, **kwargs)
        self.account.update_balance()
