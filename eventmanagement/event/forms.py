from django import forms

from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["event_title", "date_of_event", "max_participants", "teacher", "room"]
        widgets = {
            "event_title": forms.TextInput(attrs={"placeholder": "Career Talk 2026"}),
            "date_of_event": forms.DateInput(attrs={"type": "date"}),
            "max_participants": forms.NumberInput(attrs={"min": 1}),
        }


class EventUpdateForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["event_title", "date_of_event", "max_participants", "teacher", "room"]
        widgets = {
            "event_title": forms.TextInput(attrs={"placeholder": "Career Talk 2026"}),
            "date_of_event": forms.DateInput(attrs={"type": "date"}),
            "max_participants": forms.NumberInput(attrs={"min": 1}),
        }
