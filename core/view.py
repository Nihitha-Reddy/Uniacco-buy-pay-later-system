from rest_framework import viewsets
from rest_framework.response import Response
from .models import User, Purchase, RepaymentPlan, Payment, Penalty
from .serializers import UserSerializer, PurchaseSerializer, RepaymentPlanSerializer, PaymentSerializer, PenaltySerializer


# User ViewSet
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Purchase ViewSet
class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer

    def perform_create(self, serializer):
        purchase = serializer.save()
        if purchase.is_emi:
            purchase.create_repayment_plan(emi_months=12, interest_rate=10)  # Example: 12-month EMI with 10% interest


# Repayment Plan ViewSet
class RepaymentPlanViewSet(viewsets.ModelViewSet):
    queryset = RepaymentPlan.objects.all()
    serializer_class = RepaymentPlanSerializer

    def perform_create(self, serializer):
        plan = serializer.save()
        plan.generate_repayment_schedule()


# Payment ViewSet
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        payment = serializer.save()
        payment.update_credit()
        payment.apply_payment_to_plan()


# Penalty ViewSet
class PenaltyViewSet(viewsets.ModelViewSet):
    queryset = Penalty.objects.all()
    serializer_class = PenaltySerializer

    def perform_create(self, serializer):
        penalty = serializer.save()
        penalty.apply_penalty(overdue_months=1)  # Example: apply penalty for 1 month overdue
