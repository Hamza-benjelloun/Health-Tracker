# Generated by Django 3.1.7 on 2021-03-10 22:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HealthTrackerApp', '0007_auto_20210309_1744'),
    ]

    operations = [
        migrations.RenameField(
            model_name='measures',
            old_name='date_created',
            new_name='date_time',
        ),
        migrations.RenameField(
            model_name='measures',
            old_name='rfid_patient',
            new_name='id_patient',
        ),
    ]
