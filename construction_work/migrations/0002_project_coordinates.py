# Generated by Django 4.2.4 on 2023-10-12 14:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("construction_work", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="coordinates",
            field=models.JSONField(blank=True, default=None, null=True),
        ),
    ]
