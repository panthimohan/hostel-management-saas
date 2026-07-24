from django.contrib import admin

from .models import Payment, RentInvoice


@admin.register(RentInvoice)
class RentInvoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "bed_allocation", "due_date", "status", "total_amount")
    list_filter = ("status",)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "invoice", "amount", "method", "paid_on")
    list_filter = ("method",)
