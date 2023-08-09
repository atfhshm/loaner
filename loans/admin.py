from django.contrib import admin

from .models import LoanRequest, Loan, PaymentTransaction, Amortization

admin.site.register([LoanRequest, Loan, PaymentTransaction, Amortization])
