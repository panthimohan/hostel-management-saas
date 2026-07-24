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
            name="Visitor",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("visitor_name", models.CharField(max_length=255)),
                ("phone", models.CharField(blank=True, max_length=20)),
                ("purpose", models.CharField(blank=True, max_length=255)),
                ("entry_time", models.DateTimeField()),
                ("exit_time", models.DateTimeField(blank=True, null=True)),
                (
                    "hostel",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="visitors", to="hostels.hostel"),
                ),
                (
                    "logged_by",
                    models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="visitors_logged", to=settings.AUTH_USER_MODEL),
                ),
                (
                    "organization",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="visitors", to="tenants.organization"),
                ),
                (
                    "tenant_visited",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="visitors_received", to=settings.AUTH_USER_MODEL),
                ),
            ],
            options={"ordering": ["-entry_time"], "abstract": False},
        ),
        migrations.AddIndex(
            model_name="visitor",
            index=models.Index(fields=["organization", "hostel", "entry_time"], name="visitors_vis_org_hos_entry_idx"),
        ),
    ]
