# Generated by Django 3.2.12 on 2024-06-25 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='cooler',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='log',
            name='dehumidifier',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='log',
            name='heater',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='log',
            name='humidifier',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
