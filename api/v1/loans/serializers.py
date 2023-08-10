from rest_framework import serializers

from loans.models import Loan, LoanRequest, PaymentTransaction, Amortization


class RequestLoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanRequest
        fields = (
            "id",
            "requester",
            "amount",
            "term",
            "status",
            "requested_at",
            "updated_at",
        )
        read_only_fields = ("id", "status", "requested_at", "updated_at")


class ProcessLoanRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanRequest
        fields = ("id", "requester", "amount", "term", "status", "requested_at")
        read_only_fields = ("id", "requested_at", "updated_at")


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = (
            "id",
            "provider",
            "recipient",
            "employee",
            "request",
            "amount",
            "status",
            "annual_interest_rate",
            "term",
            "start_date",
            "payment_amount",
            "payment_date",
        )
        read_only_fields = ("id", "status", "payment_amount", "payment_date")


class LoanPaymentTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentTransaction
        fields = ("id", "customer", "loan", "amount")
        read_only_fields = ("id", "customer")


class AmortizationDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amortization
        fields = (
            "id",
            "loan",
            "initial_balance",
            "payment_amount",
            "interset_amount",
            "principal_amount",
            "ending_balance",
        )
