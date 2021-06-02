# Generated by Django 3.1.7 on 2021-03-10 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HealthTrackerApp', '0008_auto_20210310_2311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measures',
            name='id_patient',
            field=models.IntegerField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='measures',
            name='temperature',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='measures',
            name='tension',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
