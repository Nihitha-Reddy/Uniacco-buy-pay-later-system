from rest_framework import serializers
from .models import User, Purchase, RepaymentPlan, Payment, Penalty


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'name', 'email', 'credit_limit', 'available_credit', 'credit_score']


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ['user', 'purchase_amount', 'purchase_date', 'is_emi', 'repayment_plan']


class RepaymentPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepaymentPlan
        fields = ['user', 'purchase', 'total_amount', 'monthly_emi', 'interest_rate', 'total_months', 'penalty_rate', 'installments']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['user', 'payment_amount', 'payment_date', 'repayment_plan']


class PenaltySerializer(serializers.ModelSerializer):
    class Meta:
        model = Penalty
        fields = ['user', 'repayment_plan', 'penalty_amount', 'penalty_date']
