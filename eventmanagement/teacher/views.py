from django.contrib import messages
from django.shortcuts import redirect, render

from account.auth import login_required

from .forms import TeacherForm
from .models import Teacher


@login_required
def index(request):
    if request.method == "POST":
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Teacher record created successfully.")
            return redirect("teacher:index")
    else:
        form = TeacherForm()

    return render(
        request,
        "teacher/index.html",
        {
            "title": "Teacher",
            "description": "Create teacher profiles linked to existing teacher accounts.",
            "form": form,
            "records": Teacher.objects.select_related("account").order_by("account__username"),
            "current_account": request.account,
        },
    )
