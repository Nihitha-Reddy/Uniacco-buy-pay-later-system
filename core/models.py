from django.db import models

class User(models.Model):
    user_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    credit_limit = models.DecimalField(max_digits=10, decimal_places=2)
    available_credit = models.DecimalField(max_digits=10, decimal_places=2)
    credit_score = models.IntegerField()

    def get_available_credit(self):
        return self.available_credit

    def check_credit_limit(self, amount):
        return self.available_credit >= amount

    def __str__(self):
        return self.name


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    purchase_amount = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateField(auto_now_add=True)
    is_emi = models.BooleanField(default=False)
    repayment_plan = models.ForeignKey('RepaymentPlan', null=True, blank=True, on_delete=models.CASCADE)

    def deduct_from_credit(self):
        if self.user.check_credit_limit(self.purchase_amount):
            self.user.available_credit -= self.purchase_amount
            self.user.save()

    def create_repayment_plan(self, emi_months, interest_rate):
        if self.is_emi:
            repayment_plan = RepaymentPlan.objects.create(
                user=self.user,
                purchase=self,
                total_amount=self.purchase_amount,
                monthly_emi=self.purchase_amount / emi_months,
                interest_rate=interest_rate,
                total_months=emi_months
            )
            self.repayment_plan = repayment_plan
            self.save()


class RepaymentPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    monthly_emi = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    total_months = models.IntegerField()
    penalty_rate = models.DecimalField(max_digits=5, decimal_places=2, default=2)
    installments = models.JSONField(default=list)

    def calculate_emi(self):
        # Simple EMI formula
        principal = self.total_amount
        rate_of_interest = self.interest_rate / 12 / 100
        emi = (principal * rate_of_interest * (1 + rate_of_interest) ** self.total_months) / ((1 + rate_of_interest) ** self.total_months - 1)
        self.monthly_emi = emi
        self.save()

    def generate_repayment_schedule(self):
        # Here we could generate the repayment schedule, e.g., a list of due dates and amounts
        pass

    def calculate_penalty(self, overdue_amount):
        penalty = (overdue_amount * self.penalty_rate) / 100
        return penalty


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)
    repayment_plan = models.ForeignKey(RepaymentPlan, on_delete=models.CASCADE)

    def update_credit(self):
        self.user.available_credit += self.payment_amount
        self.user.save()

    def apply_payment_to_plan(self):
        # Apply the payment to the appropriate installment in the repayment plan
        pass


class Penalty(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    repayment_plan = models.ForeignKey(RepaymentPlan, on_delete=models.CASCADE)
    penalty_amount = models.DecimalField(max_digits=10, decimal_places=2)
    penalty_date = models.DateField(auto_now_add=True)

    def apply_penalty(self):
        self.repayment_plan.total_amount += self.penalty_amount
        self.repayment_plan.save()
