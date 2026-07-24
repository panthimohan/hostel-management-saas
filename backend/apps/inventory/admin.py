from django.contrib import admin

from .models import InventoryItem


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "quantity", "condition", "hostel")
    list_filter = ("category", "condition")
    search_fields = ("name",)
