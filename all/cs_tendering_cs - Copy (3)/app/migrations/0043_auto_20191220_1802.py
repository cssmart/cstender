# Generated by Django 2.2.7 on 2019-12-20 12:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0042_auto_20191220_1408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='componentdetails',
            name='board_detail',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.ModuleDetails'),
        ),
    ]
