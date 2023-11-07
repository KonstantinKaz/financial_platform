from rest_framework import serializers

from .models import *


class FinanceSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Account
        fields = "__all__"

    class Meta:
        model = Transaction
        fields = "__all__"
