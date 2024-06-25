from django.shortcuts import render
from django.views.generic.edit import FormView
from .models import Profile
from .forms import *
from django.contrib.auth import login
from django.contrib.auth.models import User

# Create your views here.

class EditProfile(FormView):
    form_class = RegisterForm
    template_name = "accounts/edit_profile.html"
    success_url = "/"

    def get_initial(self):
        initial = super(EditProfile, self).get_initial()
        try:
            profile = Profile.objects.get(user=self.request.user)
        except:
            profile = Profile.objects.create(user=self.request.user)
        initial.update(
            {
                "email": self.request.user.email,
                "first_name": self.request.user.first_name,
                "last_name": self.request.user.last_name,
                # "serial_no": self.request.serial_no,
                "username": self.request.user.username,
                # "activation_code": self.request.activation_code,
                # "phone": self.request.phone,
                "avatar": profile.avatar,
            }
        )
        return initial

    def form_valid(self, form):
        if form.has_changed():
            data = form.cleaned_data
            user = self.request.user
            user.first_name = data["first_name"]
            user.last_name = data["last_name"]
            user.email = data["email"]
            user.save()
            profile = Profile.objects.get(user=self.request.user)
            # profile.phone = data["phone"]
            # profile.serial_no = data["serial_no"]
            # profile.activation_code = data["activation_code"]
            profile.avatar = data["avatar"]
            profile.save()
        return super().form_valid(form)


class Register(FormView):
    form_class = RegisterForm
    template_name = "accounts/register.html"
    success_url = "/"

    def form_valid(self, form):
        data = form.cleaned_data
        if data['password1'] != data['password2']:
            form.add_error("password2", " کلمات عبور مطابقت ندارند.")
            return super().form_invalid(form)
        user = User.objects.create_user(
            username=data["phone_number"],
            password=data["password1"],
            first_name=data["first_name"],
            last_name=data["last_name"],
        )
        user.save()
        userDetail = Profile(
            user=user,
            phone_number=data["phone_number"],
        )
        userDetail.save()
        login(self.request, user)
        return super().form_valid(form)
