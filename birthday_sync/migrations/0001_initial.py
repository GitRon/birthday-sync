# Generated by Django 5.1.7 on 2025-03-30 17:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="GoogleContact",
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
                ("google_id", models.CharField(max_length=100, unique=True)),
                ("name", models.CharField(max_length=255)),
                ("birthday_day", models.PositiveSmallIntegerField()),
                ("birthday_month", models.PositiveSmallIntegerField()),
                (
                    "birthday_year",
                    models.PositiveSmallIntegerField(blank=True, null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="GoogleEvent",
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
                ("google_id", models.CharField(max_length=100, unique=True)),
                (
                    "contact",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="birthday_sync.googlecontact",
                    ),
                ),
            ],
        ),
    ]
