# Generated by Django 3.1.7 on 2021-03-11 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HealthTrackerApp', '0013_auto_20210311_0258'),
    ]

    operations = [
        migrations.CreateModel(
            name='state',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_patient', models.CharField(max_length=200, null=True)),
                ('status', models.CharField(max_length=200, null=True)),
            ],
        ),
    ]