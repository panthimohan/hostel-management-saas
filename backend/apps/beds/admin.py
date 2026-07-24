from django.contrib import admin

from .models import Bed, BedAllocation


@admin.register(Bed)
class BedAdmin(admin.ModelAdmin):
    list_display = ("id", "bed_number", "room", "status")
    list_filter = ("status",)


@admin.register(BedAllocation)
class BedAllocationAdmin(admin.ModelAdmin):
    list_display = ("id", "tenant", "bed", "check_in_date", "check_out_date")
