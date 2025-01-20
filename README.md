# Buy Now, Pay Later (BNPL) System Design

## Overview
This document outlines the design and structure of a **Buy Now, Pay Later (BNPL)** system that includes features for user registration, credit management, purchase handling, repayment scheduling, penalty calculations, and reporting.

### Assumptions:
- **Credit Limit**: Users have a fixed maximum credit limit (e.g., ₹50,000) for purchases.
- **Repayment Period**: EMI options are available for 3, 6, or 12 months.
- **Late Payment Penalty**: Penalty is charged at 2% per month on overdue payments.
- **Interest Rate**: EMI interest is based on the user's credit score (e.g., 10% annual interest).
- **Currency**: All transactions are in **INR (Indian Rupees)**.
- **EMI Calculation**: Standard EMI formula is used for calculations (based on principal, interest, and tenure).

### Core Models and Features

#### 1. **User Model**
- **Attributes**:
  - `user_id`: Unique identifier for each user.
  - `name`: Full name.
  - `email`: User's email address.
  - `credit_limit`: Maximum credit for the user (e.g., ₹50,000).
  - `available_credit`: Remaining available credit (starts equal to the credit limit).
  - `credit_score`: Credit score for determining EMI interest rates.
  
- **Methods**:
  - `get_available_credit()`: Returns the current available credit.
  - `check_credit_limit()`: Checks if the user has sufficient credit for a purchase.

#### 2. **Purchase Model**
- **Attributes**:
  - `purchase_id`: Unique identifier for the purchase.
  - `user_id`: The user making the purchase.
  - `purchase_amount`: Total amount of the purchase.
  - `purchase_date`: Date of purchase.
  - `is_emi`: Boolean indicating if the purchase is an EMI.
  - `repayment_plan`: Link to the repayment plan (if EMI).
  
- **Methods**:
  - `deduct_from_credit()`: Deducts the purchase amount from the user’s available credit.
  - `create_repayment_plan()`: Creates an EMI plan if the purchase is made on credit.

#### 3. **Repayment Plan Model**
- **Attributes**:
  - `plan_id`: Unique identifier for the repayment plan.
  - `user_id`: The user associated with the repayment plan.
  - `purchase_id`: Reference to the associated purchase.
  - `total_amount`: Total amount to be repaid (principal + interest).
  - `monthly_emi`: Monthly EMI amount.
  - `interest_rate`: Interest rate applied to the EMI.
  - `total_months`: Number of months for repayment.
  - `penalty_rate`: Late payment penalty rate.
  - `installments`: List of installments with due dates and amounts.
  
- **Methods**:
  - `calculate_emi()`: Calculates the EMI based on principal, interest, and tenure.
  - `generate_repayment_schedule()`: Generates the EMI schedule.
  - `calculate_penalty()`: Calculates the penalty for overdue payments.

#### 4. **Payment Model**
- **Attributes**:
  - `payment_id`: Unique identifier for the payment.
  - `user_id`: The user making the payment.
  - `payment_amount`: Amount paid by the user.
  - `payment_date`: Date of the payment.
  - `repayment_plan_id`: Link to the associated repayment plan.
  
- **Methods**:
  - `update_credit()`: Updates available credit after payment.
  - `apply_payment_to_plan()`: Applies payment to the correct installment in the repayment plan.

#### 5. **Penalty Model**
- **Attributes**:
  - `penalty_id`: Unique identifier for the penalty.
  - `user_id`: The user being penalized.
  - `repayment_plan_id`: The associated repayment plan.
  - `penalty_amount`: The penalty amount.
  - `penalty_date`: Date the penalty was applied.
  
- **Methods**:
  - `apply_penalty()`: Applies penalty based on overdue payments.

---

## API Endpoints

### 1. User Registration
**POST /register**

**Request Body:**
```json
{
  "user_id": "12345",
  "name": "John Doe",
  "email": "john@example.com",
  "credit_limit": 50000,
  "credit_score": 750
}
Response:

json
Copy
Edit
{
  "message": "User registered successfully."
}
2. Record a Purchase
POST /purchase

Request Body:

json
Copy
Edit
{
  "user_id": "12345",
  "purchase_amount": 10000,
  "is_emi": true,
  "emi_months": 12,
  "interest_rate": 10
}
Response:
{
  "message": "Purchase recorded successfully. Repayment plan created."
}
3. Record a Payment
POST /payment

Request Body:

{
  "user_id": "12345",
  "payment_amount": 1000,
  "repayment_plan_id": "emi_123"
}
Response:

json
Copy
Edit
{
  "message": "Payment recorded successfully."
}
4. Get Active Payment Plans and Outstanding Balance
GET /repayment_plans/{user_id}

Response:

{
  "repayment_plans": [
    {
      "plan_id": "emi_123",
      "total_amount": 12000,
      "monthly_emi": 1000,
      "outstanding_balance": 10000
    }
  ]
}
5. Get EMI-wise Outstanding Balance
GET /repayment_plans/{user_id}/emi_balance

Response:
{
  "emi_123": {
    "installment_1": {
      "due_date": "2025-02-01",
      "amount_due": 1000
    }
  }
}
6. Get Reports
GET /reports/outstanding_payments Query Parameters: start_date, end_date, user_ids, amount_range

Response:

{
  "outstanding_payments": [
    {
      "user_id": "12345",
      "repayment_plan_id": "emi_123",
      "amount_due": 5000
    }
  ]
}
7. Get Repayment History of a User
GET /repayment_history/{user_id}

Response:

{
  "repayment_history": [
    {
      "payment_date": "2025-01-15",
      "amount_paid": 1000,
      "balance_after_payment": 4000
    }
  ]
}
arduino







