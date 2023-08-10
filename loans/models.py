from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

from dateutil.relativedelta import relativedelta

__all__ = ["LoanRequest", "Loan", "PaymentTransaction", "Amortization"]


User = get_user_model()


class LoanRequest(models.Model):
    class LoanRequestStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"

    requester = models.ForeignKey(
        User,
        verbose_name=_("loan requester"),
        on_delete=models.CASCADE,
        related_name="loan_requests",
    )
    status = models.CharField(
        max_length=15,
        choices=LoanRequestStatus.choices,
        default=LoanRequestStatus.PENDING,
    )
    requested_at = models.DateTimeField(
        verbose_name=_("requested at"), auto_now_add=True
    )
    updated_at = models.DateTimeField(verbose_name=_("updated at"), auto_now=True)
    amount = models.DecimalField(
        verbose_name=_("amount"),
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(100, message=_("The minimum loan amount is 100"))
        ],
        help_text=_("the loan amount"),
    )
    term = models.PositiveIntegerField(
        verbose_name=_("loan term"), help_text=_("number of months to pay the loan")
    )

    class Meta:
        db_table = "loan_requests"
        verbose_name = _("loan request")
        verbose_name_plural = _("loan requests")

    def __str__(self) -> str:
        return f"<{self.requester}:{self.amount}>"


class Loan(models.Model):
    class LoanStatus(models.TextChoices):
        PAID = "PAID", "Paid"
        UNPAID = "UNPAID", "Unpaid"

    provider = models.ForeignKey(
        User,
        verbose_name=_("loan provider"),
        on_delete=models.CASCADE,
        related_name="provided_loans",
    )
    recipient = models.ForeignKey(
        User,
        verbose_name=_("loan recipient"),
        on_delete=models.CASCADE,
        related_name="received_loans",
    )
    employee = models.ForeignKey(
        User,
        verbose_name=_("bank employee"),
        related_name="issued_loans",
        on_delete=models.CASCADE,
    )
    request = models.OneToOneField(
        LoanRequest, verbose_name=_("loan request"), on_delete=models.CASCADE
    )
    amount = models.DecimalField(
        verbose_name=_("loan principle amount"),
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(100, message=_("The minimum loan amount is 100"))
        ],
    )
    status = models.CharField(
        max_length=15,
        choices=LoanStatus.choices,
        default=LoanStatus.UNPAID,
    )
    annual_interest_rate = models.DecimalField(
        verbose_name=_("annual interset rate"),
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(
                limit_value=1, message="interest rate can not be less than 1 (%)"
            )
        ],
    )
    term = models.PositiveIntegerField(
        verbose_name=_("loan term"), help_text=_("number of months to pay the loan")
    )
    payment_amount = models.DecimalField(
        verbose_name=_("loan payment amount"),
        max_digits=8,
        decimal_places=2,
        validators=[
            MinValueValidator(
                limit_value=1, message="interest rate can not be less than 1 (%)"
            )
        ],
        null=True,
        blank=True,
    )
    start_date = models.DateField(
        verbose_name=_("loan start date"), null=True, blank=True
    )
    payment_date = models.DateField(
        verbose_name=_("next loan payment date"), null=True, blank=True
    )
    approved_at = models.DateTimeField(verbose_name=_("approved at"), auto_now_add=True)

    class Meta:
        db_table = "loans"
        verbose_name = _("loan")
        verbose_name_plural = _("loans")

    def save(self, **kwargs) -> None:
        if not self.pk:
            self.payment_date = self.start_date + relativedelta(months=1)
        return super().save(**kwargs)

    def __str__(self) -> str:
        return f"{self.recipient}:{self.amount}"

    @property
    def monthly_interset_rate(self):
        return (self.annual_interest_rate / 100) / 12


class PaymentTransaction(models.Model):
    customer = models.ForeignKey(
        User,
        verbose_name=_("customer"),
        on_delete=models.CASCADE,
        related_name="payment_transactions",
    )
    loan = models.ForeignKey(
        Loan,
        verbose_name=_("loan"),
        on_delete=models.CASCADE,
        related_name="transactions",
    )
    amount = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[
            MinValueValidator(100, message=_("The minimum loan amount is 100"))
        ],
    )
    created_at = models.DateField(verbose_name=_("created at"), auto_now_add=True)

    class Meta:
        db_table = "payment_transactions"
        verbose_name = _("payment transaction")
        verbose_name_plural = _("payment transactions")

    def __str__(self):
        return f"{self.customer}:{self.amount}"


class Amortization(models.Model):
    loan = models.ForeignKey(
        Loan,
        verbose_name=_("loan"),
        on_delete=models.CASCADE,
        related_name="amortizations",
    )
    initial_balance = models.DecimalField(
        verbose_name=_("intial balance amount"),
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(
                limit_value=0, message="intial balance must greater or equal to 0"
            )
        ],
        null=True,
        blank=True,
    )
    payment_amount = models.DecimalField(
        verbose_name=_("payment amount"),
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(
                limit_value=0, message="payment must greater or equal to 0"
            )
        ],
        null=True,
        blank=True,
    )
    interset_amount = models.DecimalField(
        verbose_name=_("interset amount"),
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(
                limit_value=0, message="interset must greater or equal to 0"
            )
        ],
        null=True,
        blank=True,
    )

    principal_amount = models.DecimalField(
        verbose_name=_("principal amount"),
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(
                limit_value=0, message="principal must greater or equal to 0"
            )
        ],
        null=True,
        blank=True,
    )
    ending_balance = models.DecimalField(
        verbose_name=_("ending balance amount"),
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(
                limit_value=0, message="ending balance must greater or equal to 0"
            )
        ],
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "amortizations"
        verbose_name = _("amortization")
        verbose_name_plural = _("amortizations")

    def __str__(self) -> None:
        return f"{self.initial_balance}:{self.ending_balance}"
