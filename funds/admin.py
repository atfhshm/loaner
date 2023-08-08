from django.contrib import admin

from .models import Fund, FundTransaction

# admin.site.register([Fund, FundTransaction])


@admin.register(Fund)
class FundAdminConfig(admin.ModelAdmin):
    list_display = ("id", "user", "budget", "created_at", "last_deposite")


@admin.register(FundTransaction)
class FundTransactionConfig(admin.ModelAdmin):
    list_display = ("id", "user", "fund", "amount", "deposited_at")
