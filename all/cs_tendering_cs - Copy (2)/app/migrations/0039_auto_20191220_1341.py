# Generated by Django 2.2.7 on 2019-12-20 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0038_auto_20191220_1305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='componentdetails',
            name='module_detail',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
