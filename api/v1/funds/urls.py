from django.urls import path
from .views import ProviderFundView, FundTransactionView

urlpatterns = [
    path("me", ProviderFundView.as_view(), name="provider-fund"),
    path("transactions/", FundTransactionView.as_view(), name="add-transaction"),
]
