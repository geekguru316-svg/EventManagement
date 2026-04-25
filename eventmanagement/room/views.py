from django.contrib import messages
from django.shortcuts import redirect, render

from account.auth import login_required

from .forms import RoomForm
from .models import Room


@login_required
def index(request):
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Room record created successfully.")
            return redirect("room:index")
    else:
        form = RoomForm()

    return render(
        request,
        "room/index.html",
        {
            "title": "Room",
            "description": "Create and review room records used during event scheduling.",
            "form": form,
            "records": Room.objects.order_by("room_name"),
            "current_account": request.account,
        },
    )
