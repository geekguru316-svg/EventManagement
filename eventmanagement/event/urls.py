from django.urls import path

from .views import index

app_name = "event"

urlpatterns = [
    path("", index, name="index"),
]
