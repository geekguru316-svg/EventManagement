from django.urls import path

from .views import dashboard, index

app_name = "teacher"

urlpatterns = [
    path("dashboard/", dashboard, name="dashboard"),
    path("", index, name="index"),
]
