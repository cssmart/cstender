# Generated by Django 2.2.7 on 2019-12-24 06:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_moduledetails_tender_version'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='componentdetails',
            name='tender_version',
        ),
        migrations.RemoveField(
            model_name='moduledetails',
            name='tender_version',
        ),
    ]
