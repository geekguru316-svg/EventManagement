from django.urls import path

from .views import cancel_view, edit_view, index

app_name = "event"

urlpatterns = [
    path("<int:event_id>/edit/", edit_view, name="edit"),
    path("<int:event_id>/cancel/", cancel_view, name="cancel"),
    path("", index, name="index"),
]
