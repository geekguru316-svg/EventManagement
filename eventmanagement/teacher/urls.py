from django.urls import path

from .views import index

app_name = "teacher"

urlpatterns = [
    path("", index, name="index"),
]
