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


class AccountUpdateForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Leave blank to keep current password"}),
    )

    class Meta:
        model = Account
        fields = ["username", "password", "firstname", "middlename", "lastname", "type"]
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "jdoe"}),
            "firstname": forms.TextInput(attrs={"placeholder": "John"}),
            "middlename": forms.TextInput(attrs={"placeholder": "M"}),
            "lastname": forms.TextInput(attrs={"placeholder": "Doe"}),
        }

    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        qs = Account.objects.filter(username=username).exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Username is already taken.")
        return username

    def save(self, commit=True):
        account = super().save(commit=False)
        raw_password = self.cleaned_data.get("password")
        if raw_password:
            account.set_password(raw_password)
        if commit:
            account.save()
        return account


class SignupForm(forms.Form):
    ROLE_CHOICES = (
        ("S", "Student"),
        ("T", "Teacher"),
    )

    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Create password"}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirm password"}))
    firstname = forms.CharField(max_length=50)
    middlename = forms.CharField(max_length=50, required=False)
    lastname = forms.CharField(max_length=50)
    role = forms.ChoiceField(choices=ROLE_CHOICES)

    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        if Account.objects.filter(username=username).exists():
            raise forms.ValidationError("Username is already taken.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match.")

        return cleaned_data

    def save(self):
        account = Account(
            username=self.cleaned_data["username"],
            firstname=self.cleaned_data["firstname"],
            middlename=self.cleaned_data["middlename"],
            lastname=self.cleaned_data["lastname"],
            type=self.cleaned_data["role"],
        )
        account.set_password(self.cleaned_data["password"])
        account.save()
        return account
