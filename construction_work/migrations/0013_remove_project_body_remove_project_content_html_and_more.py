# Generated by Django 4.2.4 on 2023-10-10 16:28

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "construction_work",
            "0012_remove_image_filename_remove_warningmessage_images_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="project",
            name="body",
        ),
        migrations.RemoveField(
            model_name="project",
            name="content_html",
        ),
        migrations.RemoveField(
            model_name="project",
            name="coordinates",
        ),
        migrations.RemoveField(
            model_name="project",
            name="district_id",
        ),
        migrations.RemoveField(
            model_name="project",
            name="news",
        ),
        migrations.AddField(
            model_name="project",
            name="creation_date",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="project",
            name="expiration_date",
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.RemoveField(
            model_name="project",
            name="project_id",
        ),
        migrations.AddField(
            model_name="project",
            name="project_id",
            field=models.BigIntegerField(blank=False, unique=True, null=False),
        ),
        migrations.AddField(
            model_name="project",
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
            model_name="project",
            name="image",
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AddField(
            model_name="project",
            name="sections",
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AddField(
            model_name="project",
            name="timeline",
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AddField(
            model_name="project",
            name="url",
            field=models.URLField(blank=True, max_length=2048, null=True),
        ),
        migrations.AlterField(
            model_name="project",
            name="active",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="project",
            name="contacts",
            field=models.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AlterField(
            model_name="project",
            name="images",
            field=models.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AlterField(
            model_name="project",
            name="modification_date",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="project",
            name="publication_date",
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name="project",
            name="subtitle",
            field=models.CharField(blank=True, db_index=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name="project",
            name="title",
            field=models.CharField(blank=True, db_index=True, default="", max_length=1000, null=True),
        ),
    ]
