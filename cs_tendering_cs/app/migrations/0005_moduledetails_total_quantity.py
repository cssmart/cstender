# Generated by Django 2.2.7 on 2019-12-05 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20191205_1628'),
    ]

    operations = [
        migrations.AddField(
            model_name='moduledetails',
            name='total_quantity',
            field=models.CharField(default='', max_length=50),
        ),
    ]
