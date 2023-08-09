from django.contrib import admin

from .models import LoanRequest, Loan

admin.site.register([LoanRequest, Loan])