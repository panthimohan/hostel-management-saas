from django.contrib import admin

from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "hostel", "status", "preferred_check_in")
    list_filter = ("status",)
    search_fields = ("full_name", "email", "phone")
