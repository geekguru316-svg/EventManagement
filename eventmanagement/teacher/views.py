from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils import timezone

from account.auth import login_required
from event.models import Event

from .forms import TeacherAccountSettingsForm, TeacherForm, TeacherProfileSettingsForm
from .models import Teacher


@login_required
def index(request):
    if request.account.type != "A":
        return redirect("teacher:dashboard")

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


@login_required
def dashboard(request):
    if request.account.type != "T":
        messages.error(request, "Teacher access only.")
        return redirect("home")

    teacher_profile = Teacher.objects.filter(account=request.account).first()
    if request.method == "POST":
        account_form = TeacherAccountSettingsForm(request.POST, instance=request.account)
        profile_form = TeacherProfileSettingsForm(request.POST, instance=teacher_profile)
        if account_form.is_valid() and profile_form.is_valid():
            account_form.save()
            profile = profile_form.save(commit=False)
            profile.account = request.account
            profile.save()
            messages.success(request, "Profile settings updated.")
            return redirect("teacher:dashboard")
        messages.error(request, "Please correct the form errors below.")
    else:
        account_form = TeacherAccountSettingsForm(instance=request.account)
        profile_form = TeacherProfileSettingsForm(instance=teacher_profile)

    assigned_events = Event.objects.select_related("room").filter(
        teacher__account=request.account,
        date_of_event__gte=timezone.localdate(),
    ).order_by("date_of_event", "event_title")

    return render(
        request,
        "teacher/dashboard.html",
        {
            "current_account": request.account,
            "teacher_profile": teacher_profile,
            "account_form": account_form,
            "profile_form": profile_form,
            "assigned_events": assigned_events,
        },
    )
