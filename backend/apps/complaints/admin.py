from django.contrib import admin

from .models import Complaint


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ("id", "tenant", "category", "status", "created_at")
    list_filter = ("category", "status")
