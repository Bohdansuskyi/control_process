# Generated by Django 4.2.11 on 2025-07-01 20:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='station',
            name='RFID_adress',
        ),
        migrations.RemoveField(
            model_name='station',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='station',
            name='station_identification_number',
        ),
    ]
