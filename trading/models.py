from django.db import models


from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)
    gold_balance = models.DecimalField(max_digits=10, decimal_places=4, default=0)

    def __str__(self):
        return self.username


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('buy', 'Buy'),
        ('sell', 'Sell'),
    ]

    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    type = models.CharField(max_length=4, choices=TRANSACTION_TYPES)
    amount_rial = models.DecimalField(max_digits=12, decimal_places=0)
    gold_weight_gram = models.DecimalField(max_digits=10, decimal_places=4)
    price_per_gram = models.DecimalField(max_digits=12, decimal_places=0)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='completed')

    class Meta:
        indexes = [
            models.Index(fields=['user', '-date']),
        ]
        ordering = ['-date']

    def __str__(self):
        return f"{self.type} - {self.gold_weight_gram}g - User {self.user_id}"