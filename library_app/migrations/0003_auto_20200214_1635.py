# Generated by Django 3.0.3 on 2020-02-14 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("library_app", "0002_auto_20200214_1353")]

    operations = [
        migrations.AlterField(
            model_name="author",
            name="patronymic",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="author",
            name="pseudonym",
            field=models.CharField(max_length=50, unique=True),
        ),
    ]