from django.contrib import admin

from .models import TenantProfile


@admin.register(TenantProfile)
class TenantProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "university", "course")
    search_fields = ("user__email", "university", "student_id")
