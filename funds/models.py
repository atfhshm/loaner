from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

from users.models import User


class Fund(models.Model):
    # TODO: Change the on_delete action to SET_NULL after testing (null=True)
    user = models.OneToOneField(
        User, verbose_name=_("provider"), on_delete=models.CASCADE
    )
    budget = models.DecimalField(
        verbose_name=_("budget"),
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=(
            MinValueValidator(
                limit_value=0, message=_("total fund budget can not be less than 1")
            ),
        ),
    )
    created_at = models.DateTimeField(verbose_name=_("created at"), auto_now_add=True)
    last_deposite = models.DateTimeField(verbose_name=_("last_deposite"), auto_now=True)

    class Meta:
        db_table = "funds"
        verbose_name = _("fund")
        verbose_name_plural = _("funds")

    def __str__(self) -> str:
        return f"<{self.user}:{self.budget}>"


class FundTransaction(models.Model):
    # TODO: Change the on_delete action to SET_NULL after testing (null=True)
    user = models.ForeignKey(
        User,
        verbose_name=_("provider"),
        on_delete=models.CASCADE,
        related_name="fund_transactions",
    )
    # TODO: Change the on_delete action to SET_NULL after testing (null=True)
    fund = models.ForeignKey(
        Fund,
        on_delete=models.CASCADE,
        related_name="transactions",
        verbose_name=_("fund"),
    )
    amount = models.DecimalField(
        verbose_name=_("amount"),
        max_digits=8,
        decimal_places=2,
        validators=(
            MinValueValidator(
                limit_value=1, message=_("transaction amount must be greater than 1")
            ),
        ),
    )
    deposited_at = models.DateTimeField(
        verbose_name=_("deposited at"), auto_now_add=True
    )

    class Meta:
        db_table = "fund_transactions"
        verbose_name = _("fund transaction")
        verbose_name_plural = _("fund transactions")

    def __str__(self) -> str:
        return f"<{self.user}:{self.amount}>"
