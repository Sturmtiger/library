# Generated by Django 3.0.4 on 2020-03-16 09:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='bookauthorspriority',
            unique_together={('book', 'author', 'priority')},
        ),
    ]
