from django import forms

from .models import Room


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ["room_name"]
        widgets = {
            "room_name": forms.TextInput(attrs={"placeholder": "Audio Visual Room"}),
        }
