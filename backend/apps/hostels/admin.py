from django.contrib import admin

from .models import Hostel


@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "city", "country", "organization")
    list_filter = ("city", "country")
    search_fields = ("name",)
