import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
import pytz
from device.models import Device, Log
from django.http import JsonResponse
from persiantools.jdatetime import JalaliDateTime, JalaliDate
from datetime import timedelta


class logout_page(TemplateView):
    template_name = "registration/logout.html"


@login_required
def index(request):
    devices = []
    myDevices = Device.objects.filter(owner=request.user)
    tables = dataTable(myDevices)
    charts = chartsData(myDevices)
    if len(myDevices) > 0:
        for aDevice in myDevices:
            sensors = dict()

            devices.append(sensors)
    else:
        devices = False
        print(devices)
    return render(request, "dashboard/index.html", {"devices": devices, "tables": tables, "charts": charts})


def dataTable(devices):
    data = []
    for device in devices:
        deviceData = dict()
        deviceData['name'] = device.name
        logs = Log.objects.filter(device=device).order_by('-id')[:10]
        iran_timezone = pytz.timezone('Asia/Tehran')
        for log in logs:
            time = log.creation_datetime.astimezone(
                iran_timezone).strftime('%H:%M:%S')
            date = JalaliDate(log.creation_datetime).strftime('%Y/%m/%d')
            log.creation_datetime = (date + "   "+time)
        deviceData['logs'] = logs
        data.append(deviceData)
    return data


def chartsData(devices):
    colors = ['#e76c90', '#FFB6C1', '#dde1e9', "#708090", "#8A2BE2", "#800080"]
    data = []
    td = datetime.datetime.today()
    d = td - datetime.timedelta(days=7)
    x = 0
    for idx, device in enumerate(devices):
        deviceData = dict()
        deviceTemperature = []
        deviceHumidity = []
        deviceLabel = []
        # dayLogs =Log.objects.filter(device=device,creation_datetime__year =date.year, creation_datetime__month = date.month , creation_datetime__day = date.day) # Log.objects.filter(creation_datetime.date=date)
        for log in device.logs.all():
            x = x+1
            # print(x)
            # print(log.creation_datetime.time())
            deviceTemperature.append(log.temperature)
            deviceHumidity.append(log.humidity)
            iran_timezone = pytz.timezone('Asia/Tehran')
            time = log.creation_datetime.astimezone(
                iran_timezone).strftime('%H:%M:%S')
            date = JalaliDate(log.creation_datetime).strftime('%Y/%m/%d')
            deviceLabel.append(time+' '+date)
        deviceData['name'] = device.name
        deviceData['color'] = colors[idx]
        deviceData['temperature'] = deviceTemperature
        deviceData['humidity'] = deviceHumidity
        deviceData['label'] = deviceLabel
        data.append(deviceData)
    return data


def refreshData(request):
    if request.method == "GET":
        data = []
        devices = Device.objects.all()
        for device in devices:
            log = Log.objects.filter(device=device).order_by(
                "-creation_datetime")[0]
            # print(request.session[device.serial_no])
            if (log.is_seen == False):
                sensors = dict()
                sensors["name"] = device.name
                sensors["serial_no"] = device.serial_no
                if device.a1_is_active:
                    sensors["a1"] = log.analog_input_1
                if device.a2_is_active:
                    sensors["a2"] = log.analog_input_2
                if device.a3_is_active:
                    sensors["a3"] = log.analog_input_3
                if device.a4_is_active:
                    sensors["a4"] = log.analog_input_4
                if device.d1_is_active:
                    sensors["d1"] = log.digital_input_1
                if device.d2_is_active:
                    sensors["d2"] = log.digital_input_2
                if device.d3_is_active:
                    sensors["d3"] = log.digital_input_3
                if device.d4_is_active:
                    sensors["d4"] = log.digital_input_4
                if device.d5_is_active:
                    sensors["d5"] = log.digital_input_5
                if device.d6_is_active:
                    sensors["d6"] = log.digital_input_6
                data.append(sensors)
                log.is_seen = True
                log.save()
        # systemMessage = Message.objects.filter(recipient=request.user, sender=User.objects.get(username= 'mainUser'),is_read=False).last()
        # if(systemMessage):
        #     systemMessage.is_read=True
        #     systemMessage.save()
        #     return JsonResponse({"message": systemMessage.context}, status=200)
        # else:
        return JsonResponse({"data": data}, status=200)
