# Generated by Django 2.2.3 on 2020-04-11 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_frequentvisitors_visitor_registration_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='mobileregistered',
            name='f_visitor_in_time',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
