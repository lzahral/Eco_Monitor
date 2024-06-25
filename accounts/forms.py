from django import forms


class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=50, label="نام")
    last_name = forms.CharField(max_length=50, label="نام خانوادگی")
    phone_number = forms.CharField(
        min_length=11, max_length=11, label="شماره تلفن همراه")
    # username = forms.CharField(required=False,max_length=50, label="نام کاربری")
    password1 = forms.CharField(min_length=4,label="کلمه عبور")
    password2 = forms.CharField(min_length=4,label="تکرار کلمه عبور")



class messageForm(forms.Form):
    message = forms.CharField(max_length=450)
