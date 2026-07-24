from django.db import models

from utils.models import TenantModel


class ExpenseCategory(models.TextChoices):
    ELECTRICITY = "ELECTRICITY", "Electricity"
    WATER = "WATER", "Water"
    INTERNET = "INTERNET", "Internet"
    MAINTENANCE = "MAINTENANCE", "Maintenance"
    SALARY = "SALARY", "Salary"
    SUPPLIES = "SUPPLIES", "Supplies"
    CLEANING = "CLEANING", "Cleaning"
    INSURANCE = "INSURANCE", "Insurance"
    TAXES = "TAXES", "Taxes"
    MISCELLANEOUS = "MISCELLANEOUS", "Miscellaneous"


class PaymentMethod(models.TextChoices):
    CASH = "CASH", "Cash"
    BANK_TRANSFER = "BANK_TRANSFER", "Bank Transfer"
    ONLINE = "ONLINE", "Online Payment"
    CARD = "CARD", "Card"
    OTHER = "OTHER", "Other"


class Expense(TenantModel):
    """
    A single outgoing cost for a hostel. Anything that doesn't fit the
    named categories (electricity, salary, maintenance, etc.) belongs
    under MISCELLANEOUS, with the free-text `note` field used to record
    what it actually was — e.g. "Local council inspection fee".
    """

    hostel = models.ForeignKey(
        "hostels.Hostel", on_delete=models.CASCADE, related_name="expenses"
    )
    category = models.CharField(
        max_length=20, choices=ExpenseCategory.choices, default=ExpenseCategory.MISCELLANEOUS
    )
    title = models.CharField(max_length=255)
    note = models.TextField(
        blank=True,
        help_text="Especially useful for Miscellaneous expenses — describe what this actually was.",
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(
        max_length=20, choices=PaymentMethod.choices, default=PaymentMethod.CASH
    )
    receipt = models.FileField(upload_to="expense_receipts/", null=True, blank=True)
    incurred_on = models.DateField()
    recorded_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True, related_name="recorded_expenses"
    )

    class Meta:
        ordering = ["-incurred_on", "-created_at"]
        indexes = [
            models.Index(fields=["organization", "hostel", "category"]),
            models.Index(fields=["organization", "incurred_on"]),
        ]

    def __str__(self):
        return f"{self.get_category_display()} - {self.title} ({self.amount})"


class Income(TenantModel):
    """
    Non-rent income (rent itself will be tracked by the future payments
    module against BedAllocation); this covers things like registration
    fees, laundry income, vending, event-space rental, etc.
    """

    hostel = models.ForeignKey(
        "hostels.Hostel", on_delete=models.CASCADE, related_name="incomes"
    )
    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(
        max_length=20, choices=PaymentMethod.choices, default=PaymentMethod.CASH
    )
    received_on = models.DateField()
    recorded_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True, related_name="recorded_incomes"
    )

    class Meta:
        ordering = ["-received_on", "-created_at"]
        indexes = [models.Index(fields=["organization", "hostel", "received_on"])]

    def __str__(self):
        return f"{self.title} ({self.amount})"
