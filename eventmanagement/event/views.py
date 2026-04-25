from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from account.auth import login_required

from .forms import EventForm, EventUpdateForm
from .models import Event


@login_required
def index(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Event record created successfully.")
            return redirect("event:index")
    else:
        form = EventForm()

    return render(
        request,
        "event/index.html",
        {
            "title": "Event",
            "description": "Create events and assign teachers and rooms to each schedule.",
            "form": form,
            "edit_form": None,
            "edit_event": None,
            "records": Event.objects.select_related("teacher__account", "room").order_by("date_of_event", "event_title"),
            "current_account": request.account,
        },
    )


@login_required
def edit_view(request, event_id):
    record = get_object_or_404(Event, pk=event_id)
    if request.method == "POST":
        edit_form = EventUpdateForm(request.POST, instance=record)
        if edit_form.is_valid():
            edit_form.save()
            messages.success(request, "Event updated successfully.")
            return redirect("event:index")
        messages.error(request, "Please correct the form errors below.")
    else:
        edit_form = EventUpdateForm(instance=record)

    return render(
        request,
        "event/index.html",
        {
            "title": "Event",
            "description": "Create events and assign teachers and rooms to each schedule.",
            "form": EventForm(),
            "edit_form": edit_form,
            "edit_event": record,
            "records": Event.objects.select_related("teacher__account", "room").order_by("date_of_event", "event_title"),
            "current_account": request.account,
        },
    )


@login_required
def cancel_view(request, event_id):
    if request.method != "POST":
        return redirect("event:index")
    record = get_object_or_404(Event, pk=event_id)
    record.delete()
    messages.success(request, "Event cancelled successfully.")
    return redirect("event:index")
