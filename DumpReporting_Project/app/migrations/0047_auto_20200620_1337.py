# Generated by Django 2.2.3 on 2020-06-20 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0046_auto_20200620_1256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerledgerpassbook',
            name='customer',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
