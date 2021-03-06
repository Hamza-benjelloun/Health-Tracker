# Generated by Django 3.1.5 on 2021-03-08 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Firstname', models.CharField(max_length=200, null=True)),
                ('Lastname', models.CharField(max_length=200, null=True)),
                ('Cin', models.CharField(max_length=200, null=True)),
                ('State', models.CharField(max_length=200, null=True)),
                ('Temperature', models.IntegerField(max_length=200, null=True)),
                ('Tension', models.IntegerField(max_length=200, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
    ]
