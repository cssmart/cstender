# Generated by Django 2.2.9 on 2020-02-03 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20200131_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dumpreport',
            name='table_type',
            field=models.CharField(choices=[('create&insert', 'Create & Insert '), ('update', 'Update'), ('replace', 'Replace')], max_length=20),
        ),
    ]
