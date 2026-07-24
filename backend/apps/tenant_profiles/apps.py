from django.apps import AppConfig


class TenantProfilesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.tenant_profiles"
    label = "tenant_profiles"
