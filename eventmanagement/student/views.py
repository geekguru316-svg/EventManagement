from django.contrib import messages
from django.shortcuts import redirect, render

from account.auth import login_required

from .forms import StudentForm
from .models import Student


@login_required
def index(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Student record created successfully.")
            return redirect("student:index")
    else:
        form = StudentForm()

    return render(
        request,
        "student/index.html",
        {
            "title": "Student",
            "description": "Create student profiles linked to existing student accounts.",
            "form": form,
            "records": Student.objects.select_related("account").order_by("account__username"),
            "current_account": request.account,
        },
    )
