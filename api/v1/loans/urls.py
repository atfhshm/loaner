from django.urls import path
from .views import (
    RequestLoanView,
    ProcessLoanRequestView,
    LoanView,
    CustomerLoansView,
    CustomerPaymentTransactionView,
    ProviderAmortizationView,
)

urlpatterns = [
    path("requests/", RequestLoanView.as_view(), name="request-loan"),
    path(
        "loan-requests/",
        ProcessLoanRequestView.as_view(),
        name="process-loan-request",
    ),
    path("", LoanView.as_view(), name="create-list-loans"),
    path("customer/", CustomerLoansView.as_view(), name="customer-loans"),
    path(
        "payments/",
        CustomerPaymentTransactionView.as_view(),
        name="customer-payment-transactions",
    ),
    path(
        "amortizations/",
        ProviderAmortizationView.as_view(),
        name="customer-loans-amortization",
    ),
]
