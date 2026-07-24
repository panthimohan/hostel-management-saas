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
            name="AttendanceRecord",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("date", models.DateField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("PRESENT", "Present"),
                            ("ABSENT", "Absent"),
                            ("LEAVE", "Leave"),
                            ("LATE", "Late Entry"),
                        ],
                        default="PRESENT",
                        max_length=20,
                    ),
                ),
                ("note", models.CharField(blank=True, max_length=255)),
                (
                    "hostel",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="attendance_records", to="hostels.hostel"),
                ),
                (
                    "marked_by",
                    models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="attendance_marked", to=settings.AUTH_USER_MODEL),
                ),
                (
                    "organization",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="attendancerecords", to="tenants.organization"),
                ),
                (
                    "tenant",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="attendance_records", to=settings.AUTH_USER_MODEL),
                ),
            ],
            options={"ordering": ["-date"], "abstract": False},
        ),
        migrations.AddIndex(
            model_name="attendancerecord",
            index=models.Index(fields=["organization", "hostel", "date"], name="attendance_att_org_hos_date_idx"),
        ),
        migrations.AddConstraint(
            model_name="attendancerecord",
            constraint=models.UniqueConstraint(fields=("tenant", "date"), name="unique_attendance_per_tenant_per_day"),
        ),
    ]
