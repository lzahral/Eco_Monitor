from django.urls import path
from . import views

urlpatterns = [
    path("data", views.insert_log),
    path("device/<str:serial_no>", views.device_chart, name="device"),
    path("alarms", views.AddAlarm.as_view(), name="alarms"),
    path("setting/<str:serial_no>", views.Setting.as_view(), name="setting"),
    path("add-device", views.AddDevice.as_view(), name="add-device"),
    path("date-range", views.date_range, name="date-range"),
    path("device-detail/<str:serial_no>", views.device_detail, name="device-detail"),
    path("devices", views.MyDevices.as_view(), name="devices"),
]
