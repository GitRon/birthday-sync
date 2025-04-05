# Generated by Django 5.2 on 2025-04-05 12:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("birthday_sync", "0002_alter_googleevent_contact"),
    ]

    operations = [
        migrations.AlterField(
            model_name="googleevent",
            name="contact",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="birthday_sync.googlecontact",
            ),
        ),
    ]
