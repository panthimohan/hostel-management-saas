from django.db import models

from utils.models import TenantModel


class InventoryCategory(models.TextChoices):
    BED = "BED", "Bed"
    MATTRESS = "MATTRESS", "Mattress"
    CHAIR = "CHAIR", "Chair"
    TABLE = "TABLE", "Table"
    FAN = "FAN", "Fan"
    HEATER = "HEATER", "Heater"
    WASHING_MACHINE = "WASHING_MACHINE", "Washing Machine"
    OTHER = "OTHER", "Other"


class InventoryCondition(models.TextChoices):
    NEW = "NEW", "New"
    GOOD = "GOOD", "Good"
    FAIR = "FAIR", "Fair"
    DAMAGED = "DAMAGED", "Damaged"


class InventoryItem(TenantModel):
    hostel = models.ForeignKey("hostels.Hostel", on_delete=models.CASCADE, related_name="inventory_items")
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=InventoryCategory.choices, default=InventoryCategory.OTHER)
    quantity = models.PositiveIntegerField(default=1)
    condition = models.CharField(max_length=20, choices=InventoryCondition.choices, default=InventoryCondition.GOOD)
    purchase_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["hostel", "category", "name"]
        indexes = [models.Index(fields=["organization", "hostel", "category"])]

    def __str__(self):
        return f"{self.name} x{self.quantity} ({self.hostel})"
