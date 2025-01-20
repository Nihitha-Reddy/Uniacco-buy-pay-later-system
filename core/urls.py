from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register_user'),
    path('purchase/', views.record_purchase, name='record_purchase'),
    path('payment/', views.record_payment, name='record_payment'),
    path('repayment_plans/<str:user_id>/', views.get_repayment_plans, name='get_repayment_plans'),
    path('emi_balance/<str:user_id>/', views.get_emi_balance, name='get_emi_balance'),
]
