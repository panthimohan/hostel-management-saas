import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("tenants", "0001_initial"),
        ("hostels", "0001_initial"),
        ("rooms", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Reservation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("full_name", models.CharField(max_length=255)),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("phone", models.CharField(blank=True, max_length=20)),
                ("preferred_check_in", models.DateField()),
                ("preferred_check_out", models.DateField(blank=True, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("PENDING", "Pending"),
                            ("WAITLISTED", "Waitlisted"),
                            ("CONFIRMED", "Confirmed"),
                            ("CANCELLED", "Cancelled"),
                        ],
                        default="PENDING",
                        max_length=20,
                    ),
                ),
                ("notes", models.TextField(blank=True)),
                (
                    "created_by",
                    models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="reservations_created", to=settings.AUTH_USER_MODEL),
                ),
                (
                    "hostel",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="reservations", to="hostels.hostel"),
                ),
                (
                    "organization",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="reservations", to="tenants.organization"),
                ),
                (
                    "room",
                    models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="reservations", to="rooms.room"),
                ),
                (
                    "tenant",
                    models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="reservations", to=settings.AUTH_USER_MODEL),
                ),
            ],
            options={"ordering": ["-created_at"], "abstract": False},
        ),
        migrations.AddIndex(
            model_name="reservation",
            index=models.Index(fields=["organization", "hostel", "status"], name="bookings_res_org_hos_stat_idx"),
        ),
    ]
