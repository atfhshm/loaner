from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema, OpenApiParameter

from decimal import Decimal


from .serializers import (
    RequestLoanSerializer,
    ProcessLoanRequestSerializer,
    LoanSerializer,
    LoanPaymentTransactionSerializer,
    AmortizationDisplaySerializer,
)
from loans.models import Loan, LoanRequest, PaymentTransaction, Amortization
from funds.models import Fund

from users.permissions import IsCustomer, IsBanker, IsProvider


class RequestLoanView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    @extend_schema(tags=["loans"], request=RequestLoanSerializer)
    def post(self, request):
        requester = self.request.user
        payload = {
            "requester": requester.pk,
            "amount": self.request.data.get("amount"),
            "term": self.request.data.get("term"),
        }
        serializer = RequestLoanSerializer(data=payload)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.data, status=status.HTTP_406_NOT_ACCEPTABLE)

    @extend_schema(
        tags=["loans"], responses={status.HTTP_200_OK: RequestLoanSerializer(many=True)}
    )
    def get(self, request):
        loan_requests = LoanRequest.objects.filter(requester=self.request.user)
        serializer = RequestLoanSerializer(instance=loan_requests, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ProcessLoanRequestView(APIView):
    permission_classes = [IsAuthenticated, IsBanker]

    @extend_schema(
        tags=["loans"],
        responses={status.HTTP_200_OK: ProcessLoanRequestSerializer(many=True)},
    )
    def get(self, request):
        loan_requests = LoanRequest.objects.filter(status="PENDING")
        serializer = ProcessLoanRequestSerializer(instance=loan_requests, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["loans"],
        parameters=[
            OpenApiParameter(
                "r", type=int, description="the loan request id", required=True
            )
        ],
        request=ProcessLoanRequestSerializer,
        responses={status.HTTP_200_OK: ProcessLoanRequestSerializer},
    )
    def patch(self, request):
        try:
            request_id = max(int(self.request.query_params.get("r")), 0)
        except TypeError:
            return Response(
                data={"msg": "query parameter can not be empty"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        request_qs = LoanRequest.objects.filter(pk=request_id)
        if request_qs.exists():
            loan_request = request_qs.first()
            data = self.request.data
            payload = {
                "requester": loan_request.requester.pk,
                "amount": data.get("amount") or loan_request.amount,
                "term": data.get("amount") or loan_request.term,
                "status": data.get("status"),
            }
            serializer = ProcessLoanRequestSerializer(
                data=payload, instance=loan_request, partial=True
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    data=serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE
                )
        else:
            return Response(
                data={"msg": f"loan request with id = {request_id} doesn't exist"},
                status=status.HTTP_404_NOT_FOUND,
            )


class LoanView(APIView):
    permission_classes = [IsAuthenticated, IsBanker]

    @extend_schema(
        tags=["loans"],
        request=LoanSerializer,
        responses={status.HTTP_201_CREATED: LoanSerializer},
    )
    def post(self, request):
        data: dict = self.request.data

        employee = self.request.user
        provider = data.get("provider")
        recipient = data.get("recipient")
        loan_request = data.get("request")
        amount = Decimal(data.get("amount"))
        annual_interest_rate = data.get("annual_interest_rate")
        term = data.get("term")
        start_date = data.get("start_date")

        payload = {
            "provider": provider,
            "recipient": recipient,
            "employee": employee.pk,
            "request": loan_request,
            "amount": amount,
            "annual_interest_rate": annual_interest_rate,
            "term": term,
            "start_date": start_date,
        }

        provider_fund_qs = Fund.objects.filter(user=provider)
        if provider_fund_qs.exists():
            provider_fund = provider_fund_qs.first()
            if provider_fund.budget < amount:
                return Response(
                    data={"msg": "Choosen loan provider doesn't have enough budget"},
                    status=status.HTTP_409_CONFLICT,
                )
            serializer = LoanSerializer(data=payload)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    data=serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE
                )
        return Response(
            data={"msg": "Incorrect loan provider"}, status=status.HTTP_404_NOT_FOUND
        )

    @extend_schema(tags=["loans"], responses=LoanSerializer(many=True))
    def get(self, request):
        employee_loans = Loan.objects.filter(employee=self.request.user)
        serializer = LoanSerializer(instance=employee_loans, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class CustomerLoansView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LoanSerializer

    @extend_schema(tags=["loans"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        qs = Loan.objects.filter(recipient=self.request.user.pk)
        return qs


class CustomerPaymentTransactionView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsCustomer]
    serializer_class = LoanPaymentTransactionSerializer

    @extend_schema(tags=["loans"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    @extend_schema(
        tags=["loans"],
        parameters=[
            OpenApiParameter(name="l", description="loan id", type=int, required=True)
        ],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

    def get_queryset(self):
        customer = self.request.user
        loan = int(self.request.query_params.get("l"))
        qs = PaymentTransaction.objects.filter(customer=customer, loan__pk=loan)
        return qs


class ProviderAmortizationView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsProvider]
    serializer_class = AmortizationDisplaySerializer

    @extend_schema(tags=["loans"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        provider = self.request.user
        qs = Amortization.objects.select_related("loan").filter(loan__provider=provider)
        return qs
