import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("tenants", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Hostel",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=255)),
                ("address", models.CharField(max_length=500)),
                ("city", models.CharField(max_length=120)),
                ("country", models.CharField(max_length=120)),
                ("registration_number", models.CharField(blank=True, max_length=100)),
                ("license_number", models.CharField(blank=True, max_length=100)),
                ("contact_phone", models.CharField(blank=True, max_length=20)),
                ("contact_email", models.EmailField(blank=True, max_length=254)),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="hostels",
                        to="tenants.organization",
                    ),
                ),
            ],
            options={"abstract": False},
        ),
        migrations.AddIndex(
            model_name="hostel",
            index=models.Index(fields=["organization", "city"], name="hostels_hos_organiz_ab1234_idx"),
        ),
        migrations.AddConstraint(
            model_name="hostel",
            constraint=models.UniqueConstraint(fields=("organization", "name"), name="unique_hostel_name_per_org"),
        ),
    ]
