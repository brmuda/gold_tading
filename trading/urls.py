from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import TransactionViewSet, register, user_login

urlpatterns = [
    path('', TransactionViewSet.as_view({'get': 'home'}), name='home'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('transactions/buy/', TransactionViewSet.as_view({'post': 'buy'})),
    path('transactions/sell/', TransactionViewSet.as_view({'post': 'sell'})),
    path('transactions/balance/', TransactionViewSet.as_view({'get': 'get_balance'})),
    path('transactions/history/', TransactionViewSet.as_view({'get': 'get_transaction_history'}), name='transaction-history'),
]