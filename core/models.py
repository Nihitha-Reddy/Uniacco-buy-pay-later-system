from django.db import models
class User(models.Model):
   name = models.CharField(max_length=255)
   credit_limit = models.DecimalField(max_digits=10, decimal_places=2)
   available_credit = models.DecimalField(max_digits=10, decimal_places=2)
   def __str__(self):
       return self.name

class Purchase(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   amount = models.DecimalField(max_digits=10, decimal_places=2)
   date = models.DateTimeField(auto_now_add=True)
   is_em_instalment = models.BooleanField(default=False)  # Whether it's an EMI purchase
   def __str__(self):
       return f"Purchase of {self.amount} for {self.user.name}"

class RepaymentPlan(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
   number_of_months = models.IntegerField()
   interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
   monthly_installment = models.DecimalField(max_digits=10, decimal_places=2)
   penalty_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.02)  # Late payment penalty
   def calculate_total(self):
       # Calculate total repayment including interest
       total_amount = self.purchase.amount + (self.purchase.amount * (self.interest_rate / 100))
       return total_amount
   def __str__(self):
       return f"Repayment Plan for {self.purchase.amount} - {self.number_of_months} months"

class Payment(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   amount = models.DecimalField(max_digits=10, decimal_places=2)
   date = models.DateTimeField(auto_now_add=True)
   repayment_plan = models.ForeignKey(RepaymentPlan, null=True, blank=True, on_delete=models.CASCADE)
   def __str__(self):
       return f"Payment of {self.amount} for {self.user.name}"

class Penalty(models.Model):
   repayment_plan = models.ForeignKey(RepaymentPlan, on_delete=models.CASCADE)
   amount = models.DecimalField(max_digits=10, decimal_places=2)
   date = models.DateTimeField(auto_now_add=True)
   def __str__(self):
       return f"Penalty of {self.amount} for {self.repayment_plan}"
