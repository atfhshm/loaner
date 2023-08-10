from rest_framework import serializers

from funds.models import Fund, FundTransaction


class FundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fund
        fields = ("id", "budget", "created_at", "last_deposite")


class FundTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundTransaction
        fields = ("id", "amount")
        kw_args = {"id": {"read_only": "True"}}
