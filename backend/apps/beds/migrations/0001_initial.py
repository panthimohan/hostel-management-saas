import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("tenants", "0001_initial"),
        ("rooms", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Bed",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("bed_number", models.CharField(max_length=20)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("VACANT", "Vacant"),
                            ("OCCUPIED", "Occupied"),
                            ("RESERVED", "Reserved"),
                            ("MAINTENANCE", "Under Maintenance"),
                        ],
                        default="VACANT",
                        max_length=20,
                    ),
                ),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="beds",
                        to="tenants.organization",
                    ),
                ),
                (
                    "room",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="beds",
                        to="rooms.room",
                    ),
                ),
            ],
            options={"abstract": False},
        ),
        migrations.CreateModel(
            name="BedAllocation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("check_in_date", models.DateField()),
                ("check_out_date", models.DateField(blank=True, null=True)),
                ("agreement_document", models.FileField(blank=True, null=True, upload_to="agreements/")),
                (
                    "bed",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="allocations",
                        to="beds.bed",
                    ),
                ),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bedallocations",
                        to="tenants.organization",
                    ),
                ),
                (
                    "tenant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bed_allocations",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"abstract": False},
        ),
        migrations.AddIndex(
            model_name="bed",
            index=models.Index(fields=["organization", "room", "status"], name="beds_bed_organiz_ef3456_idx"),
        ),
        migrations.AddConstraint(
            model_name="bed",
            constraint=models.UniqueConstraint(fields=("room", "bed_number"), name="unique_bed_number_per_room"),
        ),
        migrations.AddIndex(
            model_name="bedallocation",
            index=models.Index(fields=["organization", "tenant"], name="beds_bedall_organiz_gh4567_idx"),
        ),
    ]
