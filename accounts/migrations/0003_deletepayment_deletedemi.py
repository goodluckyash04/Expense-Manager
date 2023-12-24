# Generated by Django 4.1.5 on 2023-09-10 15:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_emi_created_on_loan_status_alter_emi_paid_on"),
    ]

    operations = [
        migrations.CreateModel(
            name="DeletePayment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("payment_type", models.CharField(max_length=50)),
                ("category", models.CharField(default="Personal", max_length=50)),
                ("payment_date", models.DateTimeField()),
                ("amount", models.FloatField(default=0.0)),
                ("payment_for", models.CharField(max_length=50)),
                ("description", models.CharField(max_length=150)),
                ("deleted_at", models.DateTimeField(auto_now=True)),
                (
                    "payment_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="accounts.user"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DeletedEMI",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("loan", models.CharField(default=None, max_length=100)),
                ("amount", models.FloatField(default=0.0)),
                ("note", models.CharField(default=None, max_length=100)),
                ("paid_on", models.DateTimeField()),
                ("deleted_on", models.DateTimeField(auto_now=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="accounts.user"
                    ),
                ),
            ],
        ),
    ]
