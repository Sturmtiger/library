# Generated by Django 3.0.4 on 2020-03-11 13:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='created_at',
        ),
    ]
