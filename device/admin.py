from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Log)
admin.site.register(Type)
admin.site.register(Device)
admin.site.register(AlarmType)
admin.site.register(Alarms)