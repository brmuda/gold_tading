from decimal import Decimal
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render, redirect
from .models import Transaction, User
from .serializers import (
    BuyTransactionSerializer,
    SellTransactionSerializer,
    TransactionResponseSerializer,
)
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import UserLoginForm, UserRegisterForm
from django.template.loader import render_to_string
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)

PRICE_PER_GRAM = Decimal('10000000')  # 10 million rials


@method_decorator(login_required, name='dispatch')
class TransactionViewSet(viewsets.ViewSet):
    def _get_or_create_user(self, user_id):
        user, _ = User.objects.get_or_create(id=user_id)
        return user

    def home(self, request):
        transactions = Transaction.objects.filter(user=request.user).order_by('-date')
        return render(request, 'trading/home.html', {
            'transactions': transactions,
            'gold_balance': request.user.gold_balance
        })

    @action(detail=False, methods=['post'], url_path='buy')
    def buy(self, request):
        user = request.user
        logger.info(f"Buy API Request: {request.data}")
        serializer = BuyTransactionSerializer(data=request.data)

        if not serializer.is_valid():
            messages.error(request, 'داده‌های ورودی نامعتبر است')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            amount_rial = serializer.validated_data['amount_rial']
            gold_weight = Decimal(str(amount_rial)) / PRICE_PER_GRAM

            transaction = Transaction.objects.create(
                id=Transaction.objects.count() + 101,
                user=user,
                type='buy',
                amount_rial=amount_rial,
                gold_weight_gram=gold_weight,
                price_per_gram=PRICE_PER_GRAM
            )

            user.gold_balance += gold_weight
            user.save()

            response_data = {
                "transaction_id": transaction.id,
                "user_id": user.id,
                "amount_rial": float(amount_rial),
                "gold_weight_gram": float(gold_weight),
                "price_per_gram": float(PRICE_PER_GRAM),
                "status": "completed"
            }

            logger.info(f"Buy API Response: {response_data}")
            messages.success(request, 'خرید با موفقیت انجام شد')
            return Response(response_data, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Buy API Error: {str(e)}")
            messages.error(request, 'خطا در انجام تراکنش')
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='sell')
    def sell(self, request):
        user = request.user
        logger.info(f"Sell API Request: {request.data}")
        serializer = SellTransactionSerializer(data=request.data)

        if not serializer.is_valid():
            messages.error(request, 'داده‌های ورودی نامعتبر است')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            gold_weight = Decimal(str(serializer.validated_data['gold_weight_gram']))

            if user.gold_balance < gold_weight:
                messages.error(request, 'موجودی طلای شما کافی نیست')
                return Response(
                    {'error': 'Insufficient gold balance'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            amount_rial = gold_weight * PRICE_PER_GRAM

            transaction = Transaction.objects.create(
                id=Transaction.objects.count() + 101,
                user=user,
                type='sell',
                amount_rial=amount_rial,
                gold_weight_gram=gold_weight,
                price_per_gram=PRICE_PER_GRAM
            )

            user.gold_balance -= gold_weight
            user.save()

            response_data = {
                "transaction_id": transaction.id,
                "user_id": user.id,
                "gold_weight_gram": float(gold_weight),
                "amount_rial": float(amount_rial),
                "price_per_gram": float(PRICE_PER_GRAM),
                "status": "completed"
            }

            logger.info(f"Sell API Response: {response_data}")
            messages.success(request, 'فروش با موفقیت انجام شد')
            return Response(response_data, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Sell API Error: {str(e)}")
            messages.error(request, 'خطا در انجام تراکنش')
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='balance')
    def get_balance(self, request):
        user = request.user
        return Response({'balance': user.gold_balance})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'ثبت نام با موفقیت انجام شد')
            return redirect('home')
        messages.error(request, 'خطا در ثبت نام')
    else:
        form = UserRegisterForm()
    return render(request, 'trading/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, 'با موفقیت وارد شدید')
                return redirect('home')
            messages.error(request, 'نام کاربری یا رمز عبور اشتباه است')
    else:
        form = UserLoginForm()
    return render(request, 'trading/login.html', {'form': form})