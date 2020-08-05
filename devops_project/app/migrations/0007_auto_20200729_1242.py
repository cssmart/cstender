# Generated by Django 2.2.3 on 2020-07-29 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20200729_1241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(blank=True, choices=[('New', 'New'), ('WIP', 'WIP'), ('On-Hold', 'On-Hold'), ('Closed', 'Closed')], max_length=100),
        ),
    ]
