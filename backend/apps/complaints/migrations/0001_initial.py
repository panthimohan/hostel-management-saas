import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("tenants", "0001_initial"),
        ("hostels", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Complaint",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("WATER", "Water"),
                            ("ELECTRICITY", "Electricity"),
                            ("INTERNET", "Internet"),
                            ("CLEANING", "Cleaning"),
                            ("MAINTENANCE", "Maintenance"),
                            ("OTHER", "Other"),
                        ],
                        default="OTHER",
                        max_length=20,
                    ),
                ),
                ("description", models.TextField()),
                (
                    "status",
                    models.CharField(
                        choices=[("PENDING", "Pending"), ("IN_PROGRESS", "In Progress"), ("RESOLVED", "Resolved")],
                        default="PENDING",
                        max_length=20,
                    ),
                ),
                ("resolved_at", models.DateTimeField(blank=True, null=True)),
                (
                    "assigned_to",
                    models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="complaints_assigned", to=settings.AUTH_USER_MODEL),
                ),
                (
                    "hostel",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="complaints", to="hostels.hostel"),
                ),
                (
                    "organization",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="complaints", to="tenants.organization"),
                ),
                (
                    "tenant",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="complaints_filed", to=settings.AUTH_USER_MODEL),
                ),
            ],
            options={"ordering": ["-created_at"], "abstract": False},
        ),
        migrations.AddIndex(
            model_name="complaint",
            index=models.Index(fields=["organization", "hostel", "status"], name="complaints_com_org_hos_stat_idx"),
        ),
    ]
