# Generated by Django 3.0.2 on 2020-01-30 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dumpreport',
            name='sales_account',
            field=models.CharField(default='', max_length=200),
        ),
    ]
