from rest_framework import serializers
from .models import Transaction, User


class BuyTransactionSerializer(serializers.Serializer):
    amount_rial = serializers.DecimalField(max_digits=12, decimal_places=0)


class SellTransactionSerializer(serializers.Serializer):
    gold_weight_gram = serializers.DecimalField(max_digits=10, decimal_places=4)


class TransactionResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['transaction_id', 'user_id', 'amount_rial', 'gold_weight_gram',
                  'price_per_gram', 'status', 'type', 'date']

    transaction_id = serializers.IntegerField(source='id')
    user_id = serializers.IntegerField(source='user.id')