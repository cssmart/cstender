# Generated by Django 2.2.9 on 2020-02-25 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0027_auto_20200225_0459'),
    ]

    operations = [
        migrations.AddField(
            model_name='contributionreport',
            name='ladger',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
