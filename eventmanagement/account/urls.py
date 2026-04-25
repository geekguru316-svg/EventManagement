from django.urls import path

from .views import delete_view, edit_view, index, login_view, logout_view, signup_view

app_name = "account"

urlpatterns = [
    path("login/", login_view, name="login"),
    path("signup/", signup_view, name="signup"),
    path("logout/", logout_view, name="logout"),
    path("<int:account_id>/edit/", edit_view, name="edit"),
    path("<int:account_id>/delete/", delete_view, name="delete"),
    path("", index, name="index"),
]
