# Generated by Django 3.0.3 on 2020-02-17 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("library_app", "0011_auto_20200217_1222")]

    operations = [
        migrations.AddField(
            model_name="author",
            name="photo",
            field=models.ImageField(blank=True, null=True, upload_to=""),
        )
    ]
