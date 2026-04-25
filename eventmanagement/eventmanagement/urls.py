from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect, render

from account.auth import get_current_account
from account.models import Account


def home(request):
    account = get_current_account(request)
    if account is None and not Account.objects.exists():
        return redirect("account:index")
    if account is None:
        return redirect("account:login")

    return render(
        request,
        "home.html",
        {
            "current_account": account,
            "apps": [
                {"name": "Account", "path": "/account/", "summary": "User identities and roles"},
                {"name": "Student", "path": "/student/", "summary": "Student profiles and attendance"},
                {"name": "Teacher", "path": "/teacher/", "summary": "Teacher profiles and assignments"},
            ]
        },
    )


urlpatterns = [
    path('', home, name='home'),
    path('account/', include('account.urls')),
    path('student/', include('student.urls')),
    path('teacher/', include('teacher.urls')),
    path('admin/', admin.site.urls),
]
