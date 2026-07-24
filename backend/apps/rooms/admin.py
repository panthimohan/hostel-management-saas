from django.contrib import admin

from .models import Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("id", "room_number", "hostel", "room_type", "status", "price")
    list_filter = ("room_type", "status")
    search_fields = ("room_number",)
