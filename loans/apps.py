from django.apps import AppConfig


class LoansConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "loans"

    def ready(self) -> None:
        from .receivers import (
            calculate_loan_month_payment,
            create_and_update_amortization,
        )
