# Generated by Django 2.2.6 on 2019-12-28 15:05

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_tenderdatadetails_tender_creation_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tenderdatadetails',
            name='tender_creation_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 28, 15, 5, 18, 247224, tzinfo=utc)),
        ),
    ]
