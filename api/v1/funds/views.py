from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from funds.models import Fund

from .serializers import FundSerializer, FundTransactionSerializer
from users.permissions import IsProvider


__all__ = ["ProviderFundView", "FundTransactionView"]

class ProviderFundView(APIView):
    permission_classes = [IsAuthenticated, IsProvider]

    @extend_schema(tags=["funds"], responses={status.HTTP_200_OK: FundSerializer})
    def get(self, request):
        provider_fund = Fund.objects.get(user=self.request.user)
        serializer = FundSerializer(instance=provider_fund)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class FundTransactionView(APIView):
    permission_classes = [IsAuthenticated, IsProvider]

    @extend_schema(
        tags=["funds"],
        request=FundTransactionSerializer,
        responses={status.HTTP_201_CREATED: FundTransactionSerializer},
    )
    def post(self, request):
        provider = self.request.user
        payload = {
            "user": provider.pk,
            "fund": provider.fund.pk,
            "amount": self.request.data.get("amount"),
        }
        serializer = FundTransactionSerializer(data=payload)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.error_messages)
            return Response(
                data=serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE
            )
