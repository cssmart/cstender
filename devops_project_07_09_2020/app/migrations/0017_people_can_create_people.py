# Generated by Django 2.2.3 on 2020-08-29 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_project_initial_exp_completion_dt'),
    ]

    operations = [
        migrations.AddField(
            model_name='people',
            name='can_create_people',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
