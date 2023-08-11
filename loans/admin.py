from django.contrib import admin

from .models import LoanRequest, Loan, PaymentTransaction, Amortization

admin.site.register([PaymentTransaction, Amortization])

@admin.register(LoanRequest)
class LoanRequestAdminConfig(admin.ModelAdmin):
    list_display = ("id", "requester", "amount", "term", "status", "requested_at")
    

@admin.register(Loan)
class LoanAdminConfig(admin.ModelAdmin):
    fields = ("provider", "recipient", "employee", "request", "amount", "status", "term", "start_date")
    list_display = ("id", "provider", "recipient", "employee", "request", "amount", "status", "term", "payment_amount", "start_date")