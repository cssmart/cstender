# Generated by Django 2.1.13 on 2020-07-25 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20200724_1242'),
    ]

    operations = [
        migrations.AddField(
            model_name='palette_table',
            name='address',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='palette_table',
            name='label',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='palette_table',
            name='fileLink',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='palette_table',
            name='palette_category',
            field=models.CharField(choices=[('text', 'Text'), ('location', 'Location'), ('media', 'Media')], max_length=100),
        ),
    ]
