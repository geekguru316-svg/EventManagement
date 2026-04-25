from django import forms

from account.models import Account

from .models import Teacher


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ["account", "specialization", "age"]
        widgets = {
            "specialization": forms.TextInput(attrs={"placeholder": "Computer Science"}),
            "age": forms.NumberInput(attrs={"min": 18}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        used_account_ids = Teacher.objects.values_list("account_id", flat=True)
        self.fields["account"].queryset = Account.objects.filter(type="T").exclude(id__in=used_account_ids)


class TeacherAccountSettingsForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ["firstname", "middlename", "lastname"]
        widgets = {
            "firstname": forms.TextInput(attrs={"placeholder": "First name"}),
            "middlename": forms.TextInput(attrs={"placeholder": "Middle name"}),
            "lastname": forms.TextInput(attrs={"placeholder": "Last name"}),
        }


class TeacherProfileSettingsForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ["specialization", "age"]
        widgets = {
            "specialization": forms.TextInput(attrs={"placeholder": "Computer Science"}),
            "age": forms.NumberInput(attrs={"min": 18}),
        }
