# Generated by Django 2.2.7 on 2019-12-11 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20191211_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boarddetails',
            name='board_desc',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
