from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

from dateutil.relativedelta import relativedelta

from .models import Loan, PaymentTransaction, Amortization


@receiver(
    pre_save,
    sender=Loan,
)
def calculate_loan_month_payment(sender, instance: Loan, **kwargs):
    # principle amount
    p = instance.amount
    # monthly interset rate
    i = instance.monthly_interset_rate
    # term in months
    n = instance.term

    # calculate the monthly payment using amortization formula
    payment_amount = round(p * (i * (1 + i) ** n / ((1 + i) ** n - 1)))

    # update the monthly payment amount
    instance.payment_amount = payment_amount


@receiver(post_save, sender=PaymentTransaction)
def create_and_update_amortization(
    sender, instance: PaymentTransaction, created, **kwargs
):
    loan = instance.loan
    is_unpaid = loan.status == "UNPAID"
    payment = instance

    if created and is_unpaid:
        loan_amortizations = Amortization.objects.filter(loan=loan)
        if loan_amortizations.exists():
            last_amortization = loan_amortizations.last()
            initial_balance = last_amortization.ending_balance
            payment_amount = payment.amount
            interset_amount = (
                last_amortization.ending_balance * loan.monthly_interset_rate
            )
            principal_amount = payment_amount - interset_amount
            ending_balance = initial_balance - principal_amount
            ending_balance = ending_balance if ending_balance > 0 else 0

            current_amortization = Amortization(
                initial_balance=initial_balance,
                payment_amount=payment_amount,
                interset_amount=interset_amount,
                principal_amount=principal_amount,
                ending_balance=ending_balance,
                loan=loan,
            )
            current_amortization.save()
            print(ending_balance)
            if current_amortization.ending_balance == 0:
                loan.status = "PAID"

        else:
            initial_balance = loan.amount
            payment_amount = payment.amount
            interset_amount = initial_balance * loan.monthly_interset_rate
            principal_amount = payment_amount - interset_amount
            ending_balance = initial_balance - principal_amount
            ending_balance = ending_balance if ending_balance > 0 else 0
            Amortization.objects.create(
                initial_balance=initial_balance,
                payment_amount=payment_amount,
                interset_amount=interset_amount,
                principal_amount=principal_amount,
                ending_balance=ending_balance,
                loan=loan,
            )
        loan.payment_date = loan.payment_date + relativedelta(months=1)
        loan.save()
