from django import forms
from .models import Alarms


class AddDeviceForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "نام دلخواه خود را وارد کنید."}),
        max_length=50,
        label="نام دستگاه"
    )
    serial_no = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "شماره سریال نوشته شده روی دستگاه را وارد کنید."}),
        max_length=10,
        label="شماره سریال"
    )
    min_temperature = forms.IntegerField(required=False, label="حداقل دما", widget=forms.TextInput(
        attrs={"placeholder": " درصورت کمتر شدن دمای محیط از این مقدار، دستگاه هیتر روشن میشود. (مقدار دیفالت ۱۰)"}))
    max_temperature = forms.IntegerField(required=False, label="حداکثر دما", widget=forms.TextInput(
        attrs={"placeholder": " درصورت بیشتر شدن دمای محیط از این مقدار، دستگاه کولر روشن میشود. (مقدار دیفالت ۴۰)"}))
    min_humidity = forms.IntegerField(required=False, label=" حداقل رطوبت", widget=forms.TextInput(
        attrs={"placeholder": " درصورت کمتر شدن رطوبت محیط از این مقدار، دستگاه رطوبت ساز روشن میشود. (مقدار دیفالت ۳۰)"}),)
    max_humidity = forms.IntegerField(required=False, label="حداکثر رطوبت", widget=forms.TextInput(
        attrs={"placeholder": " درصورت بیشتر شدن رطوبت محیط از این مقدار، دستگاه رطوبت گیر روشن میشود. (مقدار دیفالت ۵۰)"}))


class SettingForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "نام دلخواه خود را وارد کنید."}),
        max_length=50,
        label="نام دستگاه"
    )
    min_temperature = forms.IntegerField(required=False, label="حداقل دما", widget=forms.TextInput(
        attrs={"placeholder": " درصورت کمتر شدن دمای محیط از این مقدار، دستگاه هیتر روشن میشود. (مقدار دیفالت ۱۰)"}))
    max_temperature = forms.IntegerField(required=False, label="حداکثر دما", widget=forms.TextInput(
        attrs={"placeholder": " درصورت بیشتر شدن دمای محیط از این مقدار، دستگاه کولر روشن میشود. (مقدار دیفالت ۴۰)"}))
    min_humidity = forms.IntegerField(required=False, label=" حداقل رطوبت", widget=forms.TextInput(
        attrs={"placeholder": " درصورت کمتر شدن رطوبت محیط از این مقدار، دستگاه رطوبت ساز روشن میشود. (مقدار دیفالت ۳۰)"}),)
    max_humidity = forms.IntegerField(required=False, label="حداکثر رطوبت", widget=forms.TextInput(
        attrs={"placeholder": " درصورت بیشتر شدن رطوبت محیط از این مقدار، دستگاه رطوبت گیر روشن میشود. (مقدار دیفالت ۵۰)"}))
    dehumidifier = forms.BooleanField(label='رطوبت گیر', required=False)
    humidifier = forms.BooleanField(label='رطوبت ساز', required=False)
    cooler = forms.BooleanField(label='کولر', required=False)
    heater = forms.BooleanField(label='هیتر', required=False)


class AlarmForm(forms.ModelForm):
    class Meta:
        model = Alarms
        fields = ["device", "type", "target_id", "target"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(AlarmForm, self).__init__(*args, **kwargs)
        self.fields["device"].queryset = user.devices.all()
        # self.fields['target_id'].required = False
