from django.urls import path
from . import views
urlpatterns = [
   path('register/', views.RegisterUser.as_view(), name='register'),
   path('purchase/', views.RecordPurchase.as_view(), name='record_purchase'),
   path('repayment-plan/', views.CreateRepaymentPlan.as_view(), name='create_repayment_plan'),
   path('payment/', views.RecordPayment.as_view(), name='record_payment'),
]