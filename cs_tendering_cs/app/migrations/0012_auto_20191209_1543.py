# Generated by Django 2.2.7 on 2019-12-09 10:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_remove_boarddetails_no_of_bus_section'),
    ]

    operations = [
        migrations.RenameField(
            model_name='componentdetails',
            old_name='tender_code',
            new_name='tender_id',
        ),
    ]
