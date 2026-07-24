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
            name="Expense",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("ELECTRICITY", "Electricity"),
                            ("WATER", "Water"),
                            ("INTERNET", "Internet"),
                            ("MAINTENANCE", "Maintenance"),
                            ("SALARY", "Salary"),
                            ("SUPPLIES", "Supplies"),
                            ("CLEANING", "Cleaning"),
                            ("INSURANCE", "Insurance"),
                            ("TAXES", "Taxes"),
                            ("MISCELLANEOUS", "Miscellaneous"),
                        ],
                        default="MISCELLANEOUS",
                        max_length=20,
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                (
                    "note",
                    models.TextField(
                        blank=True,
                        help_text="Especially useful for Miscellaneous expenses \u2014 describe what this actually was.",
                    ),
                ),
                ("amount", models.DecimalField(decimal_places=2, max_digits=12)),
                (
                    "payment_method",
                    models.CharField(
                        choices=[
                            ("CASH", "Cash"),
                            ("BANK_TRANSFER", "Bank Transfer"),
                            ("ONLINE", "Online Payment"),
                            ("CARD", "Card"),
                            ("OTHER", "Other"),
                        ],
                        default="CASH",
                        max_length=20,
                    ),
                ),
                ("receipt", models.FileField(blank=True, null=True, upload_to="expense_receipts/")),
                ("incurred_on", models.DateField()),
                (
                    "hostel",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="expenses",
                        to="hostels.hostel",
                    ),
                ),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="expenses",
                        to="tenants.organization",
                    ),
                ),
                (
                    "recorded_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="recorded_expenses",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"ordering": ["-incurred_on", "-created_at"], "abstract": False},
        ),
        migrations.CreateModel(
            name="Income",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(max_length=255)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=12)),
                (
                    "payment_method",
                    models.CharField(
                        choices=[
                            ("CASH", "Cash"),
                            ("BANK_TRANSFER", "Bank Transfer"),
                            ("ONLINE", "Online Payment"),
                            ("CARD", "Card"),
                            ("OTHER", "Other"),
                        ],
                        default="CASH",
                        max_length=20,
                    ),
                ),
                ("received_on", models.DateField()),
                (
                    "hostel",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="incomes",
                        to="hostels.hostel",
                    ),
                ),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="incomes",
                        to="tenants.organization",
                    ),
                ),
                (
                    "recorded_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="recorded_incomes",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"ordering": ["-received_on", "-created_at"], "abstract": False},
        ),
        migrations.AddIndex(
            model_name="expense",
            index=models.Index(fields=["organization", "hostel", "category"], name="expenses_exp_org_hos_cat_idx"),
        ),
        migrations.AddIndex(
            model_name="expense",
            index=models.Index(fields=["organization", "incurred_on"], name="expenses_exp_org_date_idx"),
        ),
        migrations.AddIndex(
            model_name="income",
            index=models.Index(fields=["organization", "hostel", "received_on"], name="expenses_inc_org_hos_date_idx"),
        ),
    ]
