from rest_framework import serializers
from rest_framework_simplejwt.authentication import JWTAuthentication


from .models import *

class IncomeCategorySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = IncomeCategory
        fields = ['id', 'user', 'title']

class ExpenseCategorySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ExpenseCategory
        fields = ['id', 'user', 'title']

class CategorySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Category
        fields = ['id', 'user', 'title', 'type']

    # Исправленный метод create

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.type = validated_data.get('type', instance.type)
        instance.save()
        return instance


class AccountSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Account  # Одна модель
        fields = "__all__"

class TransactionSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    income_category = IncomeCategorySerializer()
    expense_category = ExpenseCategorySerializer()

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



