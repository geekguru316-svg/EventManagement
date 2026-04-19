from django.contrib import messages
from django.shortcuts import redirect, render

from account.auth import login_required

from .forms import EventForm
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
            "records": Event.objects.select_related("teacher__account", "room").order_by("date_of_event", "event_title"),
            "current_account": request.account,
        },
    )
