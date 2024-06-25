from django.db import models
from django.contrib.auth.models import User


class Type(models.Model):
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.type


class Device(models.Model):
    name = models.CharField(max_length=100)
    serial_no = models.CharField(max_length=6, unique=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="devices")
    dehumidifier = models.BooleanField()
    humidifier = models.BooleanField()
    cooler = models.BooleanField()
    heater = models.BooleanField()
    max_temperature = models.IntegerField(default=40)
    min_temperature = models.IntegerField(default=10)
    max_humidity = models.IntegerField(default=50)
    min_humidity = models.IntegerField(default=30)

    def __str__(self):
        return self.name


class AlarmType(models.Model):
    type = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.type


class Alarms(models.Model):
    device = models.ForeignKey(Device,on_delete=models.CASCADE, null=True,related_name="alarms",verbose_name="دستگاه",)
    type = models.ForeignKey(AlarmType, on_delete=models.CASCADE, verbose_name="تایپ")
    target_id = models.CharField(max_length=50, verbose_name="ورودی")
    is_active = models.BooleanField(default=True)
    is_triggered = models.BooleanField(default=False)
    target = models.FloatField(null=True, blank=True, verbose_name="مقدار (ماکسیمم)")


class Log(models.Model):
    is_seen = models.BooleanField(default=False)
    creation_datetime = models.DateTimeField()
    device = models.ForeignKey( Device, on_delete=models.CASCADE, null=True, related_name="logs")
    temperature = models.FloatField(null=True, blank=True)
    humidity = models.FloatField(null=True, blank=True)
    dehumidifier = models.BooleanField(null=True, blank=True)
    humidifier = models.BooleanField(null=True, blank=True)
    cooler = models.BooleanField(null=True, blank=True)
    heater = models.BooleanField(null=True, blank=True)
