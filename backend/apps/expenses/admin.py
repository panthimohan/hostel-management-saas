from django.contrib import admin

from .models import Expense, Income


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "amount", "hostel", "incurred_on")
    list_filter = ("category", "payment_method")
    search_fields = ("title", "note")


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "amount", "hostel", "received_on")
    search_fields = ("title",)
