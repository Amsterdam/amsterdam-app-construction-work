# Generated by Django 4.2.4 on 2023-10-18 14:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("construction_work", "0003_alter_warningmessage_project_manager"),
    ]

    operations = [
        migrations.RenameField(
            model_name="article",
            old_name="article_id",
            new_name="foreign_id",
        ),
    ]
