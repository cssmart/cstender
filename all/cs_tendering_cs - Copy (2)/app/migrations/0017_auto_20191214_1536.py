# Generated by Django 2.2.7 on 2019-12-14 10:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_auto_20191214_1446'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boarddetails',
            name='board_code',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_board_models', to='app.BoardDetails'),
        ),
    ]
