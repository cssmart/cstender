# Generated by Django 2.2.3 on 2020-08-09 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20200807_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='people',
            name='can_create_application',
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AddField(
            model_name='people',
            name='can_create_project',
            field=models.BooleanField(blank=True, default=True),
        ),
    ]
