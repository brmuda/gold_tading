from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import User, Transaction

class TransactionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(gold_balance=Decimal('1.0'))

    def test_buy_gold(self):
        data = {
            'user_id': self.user.id,
            'amount_rial': 10000000
        }
        response = self.client.post('/transactions/buy/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 1)
        self.user.refresh_from_db()
        self.assertEqual(self.user.gold_balance, Decimal('2.0'))

    def test_sell_gold(self):
        data = {
            'user_id': self.user.id,
            'gold_weight_gram': 0.5
        }
        response = self.client.post('/transactions/sell/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.user.refresh_from_db()
        self.assertEqual(self.user.gold_balance, Decimal('0.5'))

    def test_sell_more_than_balance(self):
        data = {
            'user_id': self.user.id,
            'gold_weight_gram': 2.0
        }
        response = self.client.post('/transactions/sell/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_user_transactions(self):
        Transaction.objects.create(
            user=self.user,
            type='buy',
            amount_rial=10000000,
            gold_weight_gram=1.0,
            price_per_gram=10000000
        )
        response = self.client.get(f'/transactions/user/{self.user.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)