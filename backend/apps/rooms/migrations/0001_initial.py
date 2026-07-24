import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("tenants", "0001_initial"),
        ("hostels", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Room",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("room_number", models.CharField(max_length=20)),
                ("floor", models.PositiveIntegerField(default=0)),
                ("capacity", models.PositiveIntegerField(default=1)),
                (
                    "room_type",
                    models.CharField(
                        choices=[
                            ("SINGLE", "Single"),
                            ("DOUBLE", "Double"),
                            ("DORMITORY", "Dormitory"),
                            ("SUITE", "Suite"),
                        ],
                        default="SINGLE",
                        max_length=20,
                    ),
                ),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("AVAILABLE", "Available"),
                            ("FULL", "Full"),
                            ("MAINTENANCE", "Under Maintenance"),
                            ("CLOSED", "Closed"),
                        ],
                        default="AVAILABLE",
                        max_length=20,
                    ),
                ),
                (
                    "hostel",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="rooms",
                        to="hostels.hostel",
                    ),
                ),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="rooms",
                        to="tenants.organization",
                    ),
                ),
            ],
            options={"abstract": False},
        ),
        migrations.AddIndex(
            model_name="room",
            index=models.Index(fields=["organization", "hostel", "status"], name="rooms_room_organiz_cd2345_idx"),
        ),
        migrations.AddConstraint(
            model_name="room",
            constraint=models.UniqueConstraint(fields=("hostel", "room_number"), name="unique_room_number_per_hostel"),
        ),
    ]
