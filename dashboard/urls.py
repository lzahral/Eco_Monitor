from django.urls import path, include
from .views import *

urlpatterns = [
    path("", index, name="index"),
    path("refresh-data", refreshData, name="refresh-data"),
    path("logout-page", logout_page.as_view(), name="logout-page"),
]
