# Generated by Django 3.0.2 on 2020-01-30 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20200130_1742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dumpreport',
            name='from_date',
            field=models.CharField(max_length=11),
        ),
        migrations.AlterField(
            model_name='dumpreport',
            name='to_date',
            field=models.CharField(max_length=11),
        ),
    ]
