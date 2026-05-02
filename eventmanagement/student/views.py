from django.contrib import messages
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from account.auth import login_required
from event.models import Event

from .forms import StudentAccountSettingsForm, StudentForm, StudentProfileSettingsForm
from .models import AttendEvent, Student


@login_required
def index(request):
    if request.account.type != "A":
        return redirect("student:dashboard")

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


@login_required
def dashboard(request):
    if request.account.type != "S":
        messages.error(request, "Student access only.")
        return redirect("home")

    student_profile = Student.objects.filter(account=request.account).first()
    if request.method == "POST":
        account_form = StudentAccountSettingsForm(request.POST, instance=request.account)
        profile_form = StudentProfileSettingsForm(request.POST, instance=student_profile)
        if account_form.is_valid() and profile_form.is_valid():
            account_form.save()
            profile = profile_form.save(commit=False)
            profile.account = request.account
            profile.save()
            messages.success(request, "Profile settings updated.")
            return redirect("student:dashboard")
        messages.error(request, "Please correct the form errors below.")
    else:
        account_form = StudentAccountSettingsForm(instance=request.account)
        profile_form = StudentProfileSettingsForm(instance=student_profile)

    upcoming_events = list(
        Event.objects.select_related("teacher__account", "room")
        .annotate(registered_count=Count("attendevent", filter=Q(attendevent__status="Registered")))
        .filter(date_of_event__gte=timezone.localdate())
        .order_by("date_of_event", "event_title")
    )
    registered_event_ids = set()
    if student_profile is not None:
        registered_event_ids = set(
            AttendEvent.objects.filter(student=student_profile).values_list("event_id", flat=True)
        )
    for event in upcoming_events:
        event.is_registered = event.event_id in registered_event_ids
        event.is_full = event.registered_count >= event.max_participants

    return render(
        request,
        "student/dashboard.html",
        {
            "current_account": request.account,
            "student_profile": student_profile,
            "account_form": account_form,
            "profile_form": profile_form,
            "upcoming_events": upcoming_events,
        },
    )


@login_required
def register_event(request, event_id):
    if request.account.type != "S":
        messages.error(request, "Student access only.")
        return redirect("home")
    if request.method != "POST":
        return redirect("student:dashboard")

    student_profile = Student.objects.filter(account=request.account).first()
    if student_profile is None:
        messages.error(request, "Complete your student profile before registering for an event.")
        return redirect("student:dashboard")

    event = get_object_or_404(Event, pk=event_id, date_of_event__gte=timezone.localdate())
    registered_count = AttendEvent.objects.filter(event=event, status="Registered").count()
    if AttendEvent.objects.filter(student=student_profile, event=event).exists():
        messages.error(request, "You are already registered for this event.")
    elif registered_count >= event.max_participants:
        messages.error(request, "This event is already full.")
    else:
        AttendEvent.objects.create(
            student=student_profile,
            event=event,
            status="Registered",
            date_registered=timezone.localdate(),
        )
        messages.success(request, "Event registration completed.")

    return redirect("student:dashboard")
