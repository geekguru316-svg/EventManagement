from django import forms

from account.models import Account

from .models import Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["account", "course", "year", "department"]
        widgets = {
            "course": forms.TextInput(attrs={"placeholder": "BS Information Technology"}),
            "year": forms.NumberInput(attrs={"min": 1}),
            "department": forms.TextInput(attrs={"placeholder": "College of Computing"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        used_account_ids = Student.objects.values_list("account_id", flat=True)
        self.fields["account"].queryset = Account.objects.filter(type="S").exclude(id__in=used_account_ids)


class StudentAccountSettingsForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ["firstname", "middlename", "lastname"]
        widgets = {
            "firstname": forms.TextInput(attrs={"placeholder": "First name"}),
            "middlename": forms.TextInput(attrs={"placeholder": "Middle name"}),
            "lastname": forms.TextInput(attrs={"placeholder": "Last name"}),
        }


class StudentProfileSettingsForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["course", "year", "department"]
        widgets = {
            "course": forms.TextInput(attrs={"placeholder": "BS Information Technology"}),
            "year": forms.NumberInput(attrs={"min": 1}),
            "department": forms.TextInput(attrs={"placeholder": "College of Computing"}),
        }
