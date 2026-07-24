import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("tenants", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="TenantProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("photo", models.ImageField(blank=True, null=True, upload_to="tenant_photos/")),
                ("emergency_contact_name", models.CharField(blank=True, max_length=255)),
                ("emergency_contact_phone", models.CharField(blank=True, max_length=20)),
                ("address", models.CharField(blank=True, max_length=500)),
                (
                    "identification_type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("NATIONAL_ID", "National ID"),
                            ("CITIZENSHIP", "Citizenship Certificate"),
                            ("PASSPORT", "Passport"),
                            ("DRIVING_LICENSE", "Driving License"),
                            ("STUDENT_ID", "Student ID"),
                            ("WORK_PERMIT", "Work Permit"),
                        ],
                        max_length=20,
                    ),
                ),
                ("identification_number", models.CharField(blank=True, max_length=100)),
                ("identification_document_front", models.ImageField(blank=True, null=True, upload_to="tenant_identification/")),
                ("identification_document_back", models.ImageField(blank=True, null=True, upload_to="tenant_identification/")),
                ("university", models.CharField(blank=True, max_length=255)),
                ("student_id", models.CharField(blank=True, max_length=100)),
                ("course", models.CharField(blank=True, max_length=255)),
                (
                    "organization",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="tenantprofiles", to="tenants.organization"),
                ),
                (
                    "user",
                    models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="tenant_profile", to=settings.AUTH_USER_MODEL),
                ),
            ],
            options={"abstract": False},
        ),
        migrations.AddIndex(
            model_name="tenantprofile",
            index=models.Index(fields=["organization", "user"], name="tenant_prof_org_user_idx"),
        ),
    ]
