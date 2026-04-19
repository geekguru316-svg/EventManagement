from django import forms

from .models import Account


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ["username", "password", "firstname", "middlename", "lastname", "type"]
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "jdoe"}),
            "password": forms.PasswordInput(attrs={"placeholder": "Enter password"}),
            "firstname": forms.TextInput(attrs={"placeholder": "John"}),
            "middlename": forms.TextInput(attrs={"placeholder": "M"}),
            "lastname": forms.TextInput(attrs={"placeholder": "Doe"}),
        }

    def save(self, commit=True):
        account = super().save(commit=False)
        raw_password = self.cleaned_data["password"]
        account.set_password(raw_password)
        if commit:
            account.save()
        return account


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Enter password"}))
