# Generated by Django 4.2.4 on 2023-10-04 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("construction_work", "0010_remove_notification_identifier_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="image",
            name="identifier",
        ),
        migrations.RemoveField(
            model_name="image",
            name="size",
        ),
        migrations.AddField(
            model_name="image",
            name="aspect_ratio",
            field=models.FloatField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="image",
            name="coordinates",
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AddField(
            model_name="image",
            name="height",
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="image",
            name="id",
            field=models.BigAutoField(
                auto_created=True,
                default=None,
                primary_key=True,
                serialize=False,
                verbose_name="ID",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="image",
            name="width",
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name="WarningImage",
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
                ("is_main", models.BooleanField(default=False)),
                ("images", models.ManyToManyField(to="construction_work.image")),
                (
                    "warning",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="construction_work.warningmessage",
                    ),
                ),
            ],
        ),
    ]
