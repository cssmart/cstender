# Generated by Django 2.2.7 on 2019-12-11 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20191211_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boarddetails',
            name='board_desc',
            field=models.CharField(max_length=100),
        ),
    ]
