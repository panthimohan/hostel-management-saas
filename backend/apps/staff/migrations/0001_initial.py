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
            name="StaffMember",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("full_name", models.CharField(max_length=255)),
                (
                    "position",
                    models.CharField(
                        choices=[
                            ("MANAGER", "Manager"),
                            ("RECEPTIONIST", "Receptionist"),
                            ("ACCOUNTANT", "Accountant"),
                            ("CLEANER", "Cleaner"),
                            ("SECURITY", "Security"),
                            ("COOK", "Cook"),
                            ("OTHER", "Other"),
                        ],
                        default="OTHER",
                        max_length=20,
                    ),
                ),
                ("phone", models.CharField(blank=True, max_length=20)),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("salary", models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ("hire_date", models.DateField(blank=True, null=True)),
                (
                    "status",
                    models.CharField(choices=[("ACTIVE", "Active"), ("INACTIVE", "Inactive")], default="ACTIVE", max_length=20),
                ),
                (
                    "hostel",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="staff_members", to="hostels.hostel"),
                ),
                (
                    "organization",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="staffmembers", to="tenants.organization"),
                ),
                (
                    "user",
                    models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="staff_record", to=settings.AUTH_USER_MODEL),
                ),
            ],
            options={"ordering": ["full_name"], "abstract": False},
        ),
        migrations.AddIndex(
            model_name="staffmember",
            index=models.Index(fields=["organization", "hostel", "position"], name="staff_staf_org_hos_pos_idx"),
        ),
    ]
