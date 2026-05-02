from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils import timezone

from account.auth import login_required
from event.forms import TeacherEventForm
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
    if request.method == "POST" and request.POST.get("form_type") == "profile":
        account_form = TeacherAccountSettingsForm(request.POST, instance=request.account)
        profile_form = TeacherProfileSettingsForm(request.POST, instance=teacher_profile)
        event_form = TeacherEventForm()
        if account_form.is_valid() and profile_form.is_valid():
            account_form.save()
            profile = profile_form.save(commit=False)
            profile.account = request.account
            profile.save()
            messages.success(request, "Profile settings updated.")
            return redirect("teacher:dashboard")
        messages.error(request, "Please correct the form errors below.")
    elif request.method == "POST" and request.POST.get("form_type") == "event":
        account_form = TeacherAccountSettingsForm(instance=request.account)
        profile_form = TeacherProfileSettingsForm(instance=teacher_profile)
        event_form = TeacherEventForm(request.POST)
        if teacher_profile is None:
            messages.error(request, "Complete your teacher profile before creating an event.")
        elif event_form.is_valid():
            event = event_form.save(commit=False)
            event.teacher = teacher_profile
            event.save()
            messages.success(request, "Event created successfully.")
            return redirect("teacher:dashboard")
        else:
            messages.error(request, "Please correct the event form errors below.")
    else:
        account_form = TeacherAccountSettingsForm(instance=request.account)
        profile_form = TeacherProfileSettingsForm(instance=teacher_profile)
        event_form = TeacherEventForm()

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
            "event_form": event_form,
            "assigned_events": assigned_events,
        },
    )
