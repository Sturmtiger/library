# Generated by Django 3.0.3 on 2020-03-03 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_app', '0005_auto_20200303_0939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='type',
            field=models.IntegerField(blank=True, choices=[(1, 'admin'), (2, 'publisher'), (3, 'reader')], null=True),
        ),
    ]
