from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_user_organization"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="role",
            field=models.CharField(
                choices=[
                    ("SUPER_ADMIN", "Super Admin"),
                    ("HOSTEL_OWNER", "Hostel Owner"),
                    ("HOSTEL_MANAGER", "Hostel Manager"),
                    ("RECEPTIONIST", "Receptionist"),
                    ("ACCOUNTANT", "Accountant"),
                    ("TENANT", "Tenant"),
                ],
                default="TENANT",
                max_length=20,
            ),
        ),
    ]
