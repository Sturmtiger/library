# Generated by Django 3.0.4 on 2020-03-16 11:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library_app', '0005_auto_20200316_1334'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='bookauthorspriority',
            unique_together=set(),
        ),
    ]
