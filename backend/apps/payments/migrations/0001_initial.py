import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("tenants", "0001_initial"),
        ("beds", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="RentInvoice",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("billing_period_start", models.DateField()),
                ("billing_period_end", models.DateField()),
                ("due_date", models.DateField()),
                ("rent_amount", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("security_deposit", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("utility_amount", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("late_fee", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("UNPAID", "Unpaid"),
                            ("PARTIALLY_PAID", "Partially Paid"),
                            ("PAID", "Paid"),
                            ("OVERDUE", "Overdue"),
                        ],
                        default="UNPAID",
                        max_length=20,
                    ),
                ),
                (
                    "bed_allocation",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="invoices", to="beds.bedallocation"),
                ),
                (
                    "organization",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="rentinvoices", to="tenants.organization"),
                ),
            ],
            options={"ordering": ["-due_date"], "abstract": False},
        ),
        migrations.CreateModel(
            name="Payment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "method",
                    models.CharField(
                        choices=[
                            ("CASH", "Cash"),
                            ("BANK_TRANSFER", "Bank Transfer"),
                            ("CREDIT_CARD", "Credit Card"),
                            ("STRIPE", "Stripe"),
                            ("PAYPAL", "PayPal"),
                        ],
                        default="CASH",
                        max_length=20,
                    ),
                ),
                ("reference_number", models.CharField(blank=True, max_length=100)),
                ("paid_on", models.DateField()),
                (
                    "invoice",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="payments", to="payments.rentinvoice"),
                ),
                (
                    "organization",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="payments", to="tenants.organization"),
                ),
                (
                    "recorded_by",
                    models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="recorded_payments", to=settings.AUTH_USER_MODEL),
                ),
            ],
            options={"ordering": ["-paid_on"], "abstract": False},
        ),
        migrations.AddIndex(
            model_name="rentinvoice",
            index=models.Index(fields=["organization", "status", "due_date"], name="payments_inv_org_stat_due_idx"),
        ),
        migrations.AddIndex(
            model_name="payment",
            index=models.Index(fields=["organization", "invoice"], name="payments_pay_org_inv_idx"),
        ),
    ]
