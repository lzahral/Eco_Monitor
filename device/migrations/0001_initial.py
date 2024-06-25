# Generated by Django 3.2.12 on 2024-06-24 22:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AlarmType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=50)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('serial_no', models.CharField(max_length=6, unique=True)),
                ('dehumidifier', models.BooleanField()),
                ('humidifier', models.BooleanField()),
                ('cooler', models.BooleanField()),
                ('heater', models.BooleanField()),
                ('max_temperature', models.IntegerField(default=40)),
                ('min_temperature', models.IntegerField(default=10)),
                ('max_humidity', models.IntegerField(default=50)),
                ('min_humidity', models.IntegerField(default=30)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='devices', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_seen', models.BooleanField(default=False)),
                ('creation_datetime', models.DateTimeField()),
                ('temperature', models.FloatField(blank=True, null=True)),
                ('humidity', models.FloatField(blank=True, null=True)),
                ('dehumidifier', models.BooleanField()),
                ('humidifier', models.BooleanField()),
                ('cooler', models.BooleanField()),
                ('heater', models.BooleanField()),
                ('device', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='device.device')),
            ],
        ),
        migrations.CreateModel(
            name='Alarms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target_id', models.CharField(max_length=50, verbose_name='ورودی')),
                ('is_active', models.BooleanField(default=True)),
                ('is_triggered', models.BooleanField(default=False)),
                ('target', models.FloatField(blank=True, null=True, verbose_name='مقدار (ماکسیمم)')),
                ('device', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='alarms', to='device.device', verbose_name='دستگاه')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='device.alarmtype', verbose_name='تایپ')),
            ],
        ),
    ]