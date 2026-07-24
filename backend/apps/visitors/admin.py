from django.contrib import admin

from .models import Visitor


@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ("id", "visitor_name", "tenant_visited", "entry_time", "exit_time")
    search_fields = ("visitor_name", "phone")
