from django.contrib import admin
from .models import User, Transaction

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'gold_balance')
    search_fields = ('id',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'type', 'amount_rial', 'gold_weight_gram', 'date', 'status')
    list_filter = ('type', 'status', 'date')
    search_fields = ('user__id',)