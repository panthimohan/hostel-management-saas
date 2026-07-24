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
            name="InventoryItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=255)),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("BED", "Bed"),
                            ("MATTRESS", "Mattress"),
                            ("CHAIR", "Chair"),
                            ("TABLE", "Table"),
                            ("FAN", "Fan"),
                            ("HEATER", "Heater"),
                            ("WASHING_MACHINE", "Washing Machine"),
                            ("OTHER", "Other"),
                        ],
                        default="OTHER",
                        max_length=20,
                    ),
                ),
                ("quantity", models.PositiveIntegerField(default=1)),
                (
                    "condition",
                    models.CharField(
                        choices=[("NEW", "New"), ("GOOD", "Good"), ("FAIR", "Fair"), ("DAMAGED", "Damaged")],
                        default="GOOD",
                        max_length=20,
                    ),
                ),
                ("purchase_date", models.DateField(blank=True, null=True)),
                ("notes", models.TextField(blank=True)),
                (
                    "hostel",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="inventory_items", to="hostels.hostel"),
                ),
                (
                    "organization",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="inventoryitems", to="tenants.organization"),
                ),
            ],
            options={"ordering": ["hostel", "category", "name"], "abstract": False},
        ),
        migrations.AddIndex(
            model_name="inventoryitem",
            index=models.Index(fields=["organization", "hostel", "category"], name="inventory_inv_org_hos_cat_idx"),
        ),
    ]
