# Generated by Django 3.0.2 on 2020-01-24 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='erpreport',
            name='from_data',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='erpreport',
            name='to_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
