from django.dispatch import receiver
from django.db.models.signals import post_save
from decimal import Decimal

from .models import Loan


@receiver(
    post_save,
    sender=Loan,
)
def calculate_loan_month_payment(sender, instance: Loan, created, **kwargs):
    # principle amount
    p = instance.amount
    # monthly interset rate
    i = (instance.annual_interest_rate / 100) / 12
    # term in months
    n = instance.term

    payment_amount = p * (i * (1 + i) ** n / ((1 + i) ** n - 1))

    if created:
        instance.payment_amount = round(payment_amount)
        instance.save()
