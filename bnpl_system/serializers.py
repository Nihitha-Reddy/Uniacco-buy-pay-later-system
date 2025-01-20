from rest_framework import serializers
from .models import User, Purchase, RepaymentPlan, Payment
class UserSerializer(serializers.ModelSerializer):
   class Meta:
       model = User
       fields = ['id', 'name', 'credit_limit', 'available_credit']

class PurchaseSerializer(serializers.ModelSerializer):
   class Meta:
       model = Purchase
       fields = ['id', 'user', 'amount', 'date', 'is_em_instalment']

class RepaymentPlanSerializer(serializers.ModelSerializer):
   class Meta:
       model = RepaymentPlan
       fields = ['id', 'user', 'purchase', 'number_of_months', 'interest_rate', 'monthly_installment']

class PaymentSerializer(serializers.ModelSerializer):
   class Meta:
       model = Payment
       fields = ['id', 'user', 'amount', 'date', 'repayment_plan']