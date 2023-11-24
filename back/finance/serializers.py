from rest_framework import serializers

from .models import *

class AccountSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Account  # Одна модель
        fields = "__all__"

class TransactionSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Сумма должна быть положительной.")
        return value

    def validate_description(self, value):
        if not isinstance(value, str):
            raise serializers.ValidationError("Описание должно быть строкой.")
        return value

    def validate(self, data):
        if data['amount'] <= 0:
            raise serializers.ValidationError({"amount": ["Сумма должна быть положительной."]})

        if 'description' in data and not isinstance(data['description'], str):
            raise serializers.ValidationError({"description": ["Описание должно быть строкой."]})

        return data

    class Meta:
        model = Transaction
        fields = "__all__"


class IncomeCategorySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = IncomeCategory
        fields = "__all__"


class ExpenseCategorySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ExpenseCategory
        fields = "__all__"