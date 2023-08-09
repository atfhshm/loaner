from django.contrib import admin

from .models import LoanRequest, Loan, PaymentTransaction

admin.site.register([LoanRequest, Loan, PaymentTransaction])
