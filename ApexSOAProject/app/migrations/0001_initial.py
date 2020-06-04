# Generated by Django 2.2.3 on 2020-05-12 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApexTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trx_label', models.IntegerField(blank=True)),
                ('forwarded_to', models.IntegerField(blank=True)),
                ('forwarded_by', models.IntegerField(blank=True)),
                ('item_template', models.CharField(blank=True, max_length=200)),
                ('apex_id', models.IntegerField(blank=True)),
            ],
        ),
    ]
