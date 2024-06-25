import datetime
from django.contrib.auth import authenticate
from django.views.generic.base import TemplateView
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView, CreateView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from persiantools.jdatetime import JalaliDateTime, JalaliDate
from .models import *
from .forms import *
from persiantools import characters, digits

import pytz

def device_detail(request, serial_no):
    # logs = []
    device = Device.objects.get(serial_no=serial_no)
    # device_logs = Log.objects.filter(device=device).order_by("-creation_datetime")
    # for log in device_logs:
    #     sensors = dict()
    #     sensors["date"] = JalaliDate(log.creation_datetime.date())
    #     sensors["time"] = log.creation_datetime.astimezone()
    #     if log.analog_input_1 == None:
    #         sensors["a1"] = "-"
    #     else:
    #         sensors["a1"] = log.analog_input_1

    #     if log.analog_input_2 == None:
    #         sensors["a2"] = "-"
    #     else:
    #         sensors["a2"] = log.analog_input_2

    #     if log.analog_input_3 == None:
    #         sensors["a3"] = "-"
    #     else:
    #         sensors["a3"] = log.analog_input_3

    #     if log.analog_input_4 == None:
    #         sensors["a4"] = "-"
    #     else:
    #         sensors["a4"] = log.analog_input_4
    #     sensors["d1"] = log.digital_input_1
    #     sensors["d2"] = log.digital_input_2
    #     sensors["d3"] = log.digital_input_3
    #     sensors["d4"] = log.digital_input_4
    #     sensors["d5"] = log.digital_input_5
    #     sensors["d6"] = log.digital_input_6
    #     logs.append(sensors)
    # # paginator = Paginator(sensors, 25)  # Show 25 contacts per page.
    # chartLogs = chart_logs(device)
    # tLogs = chartLogs[len(chartLogs) - 1]
    devices = []
    myDevices = Device.objects.filter(owner=request.user)

    # tables = dataTable(myDevices)
    charts = chartsData(myDevices)
    return render(
        request,
        "device/device_detail.html",
        {"device": device,  "chartLogs": charts},
    )




def chart_logs(device, td=datetime.datetime.today(), days=30):
    chartLogs = []
    for d in (
        td - datetime.timedelta(days=x) for x in range(0, days)
    ):
        date =d.date() # datetime.date(day=d.day, year=d.year, month=d.month)
        dayLogs =Log.objects.filter(device=device,creation_datetime__year =date.year, creation_datetime__month = date.month , creation_datetime__day = date.day) # Log.objects.filter(creation_datetime.date=date)
        if len(dayLogs) > 0:
            dLogs = dict()
            dLogs["date"] = JalaliDate(date).strftime('%Y/%m/%d')
            on = [0, 0, 0, 0, 0, 0]
            for y in reversed(range(0, len(dayLogs) - 1, 1)):
                time1 = dayLogs[y + 1].creation_datetime
                time2 = dayLogs[y].creation_datetime
                time = int((time1 - time2).total_seconds() / 60)
                if dayLogs[y].digital_input_1:
                    on[0] += time
                if dayLogs[y].digital_input_2:
                    on[1] += time
                if dayLogs[y].digital_input_3:
                    on[2] += time
                if dayLogs[y].digital_input_4:
                    on[3] += time
                if dayLogs[y].digital_input_5:
                    on[4] += time
                if dayLogs[y].digital_input_6:
                    on[5] += time

            dLogs["on"] = on
            chartLogs.insert(0, dLogs)
    return(chartLogs)

def date_range(request):
    serial_no=request.POST.get('device')
    device = Device.objects.get(serial_no=serial_no)

    from_date = request.POST.get('fd').split('/')
    to_date = request.POST.get('td').split('/')
    fd = JalaliDateTime(int(from_date[0]), int(from_date[1]), int(from_date[2]))
    td = JalaliDateTime(int(to_date[0]), int(to_date[1]), int(to_date[2]))
    days=(td.date()-fd.date()).days+1
    chartLogs = chart_logs(device,td,days)
    return JsonResponse({"chartLogs": chartLogs}, status=200)

@login_required(login_url="login")
def device_chart(request,serial_no):
    devices = []
    device = Device.objects.get(serial_no=serial_no)
    devices.append(device)
    if request.method == "GET":
        # data = chart_logs(device)
        # devices = []
        charts = chartsData(devices)
        context = {
            "charts": charts,
            "serial_no":serial_no
            }
        return render(request, "device/device.html", context)    
    else:
        try:
            from_date = request.POST.get('fd').split('/')
            to_date = request.POST.get('td').split('/')
            fd = JalaliDate(int(from_date[0]), int(
                from_date[1]), int(from_date[2])).to_gregorian()

            td = JalaliDate(int(to_date[0]), int(
                to_date[1]), int(to_date[2])).to_gregorian()
            if td > fd:
                print(request.POST.get('fd'))
                print(devices)
                chartLogs = chartsData(devices,fd,td)
                print(chart_logs)
                context = {
                    "chartLogs": chartLogs,
                    "serial_no": serial_no
                }
                return JsonResponse(context, status=200)
        except:
            context = {
                "message": "بازه زمانی انتخابی شما اشتباه می‌باشد! لطفا در انتخاب بازه زمانی دقت کنید."
                , "serial_no": serial_no
            }

        return render(request, "device/device.html", context)


def chartsData(devices, sd=False, fd=False):
    
    colors = ['#e76c90', '#FFB6C1', '#dde1e9', "#708090", "#8A2BE2", "#800080"]
    data = []
    td = datetime.datetime.today()
    d = td - datetime.timedelta(days=7)
    x = 0
    if sd == False:
        print('ji')
        logs = devices[0].logs.all().order_by("creation_datetime")
    else:
        print(sd)
        logs = devices[0].logs.filter(creation_datetime__range=[sd, fd])
        print(logs)
    for idx, device in enumerate(devices):
        deviceData = dict()
        deviceTemperature = []
        deviceHumidity = []
        deviceLabel = []
        for log in logs:
            x = x+1
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

class MyDevices(ListView):
    template_name = "device/devices.html"
    context_object_name = "devices"
    model = Device

    def get_queryset(self):
        queryset = Device.objects.filter(owner=self.request.user)
        return queryset

class DeviceDetail(DetailView):
    template_name = "products/product.html"
    model = Device

class myDevice(TemplateView):
    template_name = "device/device.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        serial_no = kwargs['serial_no']
        device = self.request.user.devices.get(serial_no=serial_no)
        print(device)
        data = chart_logs(device)
        context["device"] = device.serial_no
        context["chartLogs"] = data
        return context

class Setting(FormView):
    form_class = SettingForm
    template_name = "device/setting.html"
    success_url = "/device/devices"

    def get_initial(self):
        serial_no = self.kwargs["serial_no"]
        initial = super(Setting, self).get_initial()
        device = Device.objects.get(serial_no=serial_no)
        initial.update(
            {
                "name": device.name,
                "min_temperature": device.min_temperature,
                "max_temperature": device.max_temperature,
                "min_humidity": device.min_humidity,
                "max_humidity": device.max_humidity,
                "dehumidifier": device.dehumidifier,
                "humidifier": device.humidifier,
                "cooler": device.cooler,
                "heater": device.heater,
            }
        )
        return initial

    def form_valid(self, form):
        if form.has_changed():
            data = form.cleaned_data
            serial_no = self.kwargs["serial_no"]
            device = Device.objects.get(serial_no=serial_no)
            device.name = data["name"]
            device.min_temperature = data["min_temperature"]
            device.max_temperature = data["max_temperature"]
            device.min_humidity = data["min_humidity"]
            device.max_humidity = data["max_humidity"]
            device.dehumidifier = data["dehumidifier"]
            device.humidifier = data["humidifier"]
            device.cooler = data["cooler"]
            device.heater = data["heater"]
            device.save()
        return super().form_valid(form)

class AddDevice(FormView):
    form_class = AddDeviceForm
    template_name = "device/add_device.html"
    success_url = "/device/devices"

    def form_valid(self, form):
        serial_no = form.cleaned_data["serial_no"]
        if serial_no == "":
            form.add_error("serial_no", "شماره سریال را وارد کنید.")
        serial_no = f'{digits.fa_to_en(serial_no)}'
        if Device.objects.filter(serial_no=serial_no).exists():
            device = Device.objects.get(serial_no=serial_no)
            if device.owner.is_superuser:
                form.clean()
                device.owner = self.request.user 
                if form.cleaned_data["name"] != '':
                    device.name = form.cleaned_data["name"]
                if form.cleaned_data["min_temperature"] != None:
                    device.min_temperature = form.cleaned_data["min_temperature"]
                if form.cleaned_data["max_temperature"] != None:
                    device.max_temperature = form.cleaned_data["max_temperature"]
                if form.cleaned_data["min_humidity"] != None:
                    device.min_humidity = form.cleaned_data["min_humidity"]
                if form.cleaned_data["max_humidity"] != None:
                    device.max_humidity = form.cleaned_data["max_humidity"]
                device.save()
                return super().form_valid(form)           
            else:
                form.add_error("serial_no", "َشماره سریال  نامعتبر است.")
        elif serial_no != "":
            form.add_error("serial_no", "َشماره سریال  نامعتبر است.")
        return super().form_invalid(form)

class AddAlarm(FormView):
    template_name = "device/alarm.html"
    success_url = "/device/alarms"
    form_class = AlarmForm

    def get_form_kwargs(self):
        kwargs = super(AddAlarm, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data=''
        devices = self.request.user.devices.all()
        for device in devices:
            alarms = device.alarms.all()
            if data !='':
                data = data.union(alarms)
            else:
                data=alarms
        context["alarms"] = data
        return context
    
    def get_initial(self):
        initial = super(AddAlarm, self).get_initial()
        initial.update({'type':'1'})
        return initial
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


def insert_log(req):
    if req.method == "GET":
        # print(req)
        serial_no = req.GET["serial_no"]
        date = req.GET["date"]
        time = req.GET["time"]
        date_time = date+" "+time
        date_time = datetime.datetime.strptime(date_time,"%Y-%m-%d %H:%M:%S.%f")
        temperature = req.GET["temperature"]
        humidity = req.GET["humidity"]
        device = Device.objects.get(serial_no=serial_no)
        log = Log.objects.create(
            device=device,
            creation_datetime=date_time,
            temperature=temperature,
            humidity=humidity,
        )
        log.save()
    return JsonResponse({"message": 'incorrect data'}, status=200)