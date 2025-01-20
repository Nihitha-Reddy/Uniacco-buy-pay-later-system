from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, Purchase, RepaymentPlan, Payment
from .serializers import UserSerializer, PurchaseSerializer, RepaymentPlanSerializer, PaymentSerializer
class RegisterUser(APIView):
   def post(self, request):
       serializer = UserSerializer(data=request.data)
       if serializer.is_valid():
           user = serializer.save()
           return Response({"id": user.id, "name": user.name}, status=status.HTTP_201_CREATED)
       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RecordPurchase(APIView):
   def post(self, request):
       user = User.objects.get(id=request.data["user_id"])
       purchase_amount = request.data["amount"]
       if user.available_credit >= purchase_amount:
           purchase = Purchase.objects.create(user=user, amount=purchase_amount)
           user.available_credit -= purchase_amount
           user.save()
           return Response({"purchase_id": purchase.id}, status=status.HTTP_201_CREATED)
       return Response({"error": "Insufficient credit"}, status=status.HTTP_400_BAD_REQUEST)

class CreateRepaymentPlan(APIView):
   def post(self, request):
       purchase = Purchase.objects.get(id=request.data["purchase_id"])
       user = purchase.user
       months = request.data["number_of_months"]
       interest_rate = request.data["interest_rate"]
       emi_amount = (purchase.amount + (purchase.amount * (interest_rate / 100))) / months
       repayment_plan = RepaymentPlan.objects.create(
           user=user,
           purchase=purchase,
           number_of_months=months,
           interest_rate=interest_rate,
           monthly_installment=emi_amount
       )
       return Response({"repayment_plan_id": repayment_plan.id}, status=status.HTTP_201_CREATED)

class RecordPayment(APIView):
   def post(self, request):
       user = User.objects.get(id=request.data["user_id"])
       amount = request.data["amount"]
       payment = Payment.objects.create(user=user, amount=amount)
       user.available_credit += amount
       user.save()
       return Response({"payment_id": payment.id}, status=status.HTTP_201_CREATED)