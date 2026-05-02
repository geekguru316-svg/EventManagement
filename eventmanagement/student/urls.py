from django.urls import path

from .views import dashboard, index, register_event

app_name = "student"

urlpatterns = [
    path("dashboard/", dashboard, name="dashboard"),
    path("events/<int:event_id>/register/", register_event, name="register_event"),
    path("", index, name="index"),
]
