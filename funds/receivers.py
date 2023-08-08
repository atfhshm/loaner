from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import FundTransaction


@receiver(post_save, sender=FundTransaction)
def update_fund_budget(
    sender, instance: FundTransaction, created: bool, *args, **kwargs
):
    """Add the fund trasaction amount to the fund total budget"""
    fund = instance.fund
    transaction = instance

    if created:
        fund.budget += transaction.amount
        fund.save()
