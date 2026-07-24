from django.contrib import admin

from .models import StaffMember


@admin.register(StaffMember)
class StaffMemberAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "position", "hostel", "status")
    list_filter = ("position", "status")
    search_fields = ("full_name", "email", "phone")
