# Generated by Django 3.1.5 on 2021-03-08 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HealthTrackerApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='State',
            field=models.CharField(choices=[('Sleeping', 'Sleeping'), ('Falling', 'Falling'), ('Standing', 'Standing'), ('Sitting', 'Sitting')], max_length=200),
        ),
    ]
