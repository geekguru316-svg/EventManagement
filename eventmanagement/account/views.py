from django.contrib import messages
from django.shortcuts import redirect, render

from .auth import get_current_account, login_required
from .forms import AccountForm, LoginForm
from .models import Account


def login_view(request):
    if not Account.objects.exists():
        messages.info(request, "Create the first account to enable login.")
        return redirect("account:index")

    if get_current_account(request):
        return redirect("home")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            account = Account.objects.filter(username=username).first()
            if account and account.verify_password(password):
                request.session["account_id"] = account.id
                messages.success(request, f"Welcome, {account.firstname}.")
                return redirect("home")
            messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()

    return render(request, "account/login.html", {"form": form})


def logout_view(request):
    request.session.pop("account_id", None)
    messages.success(request, "You have been logged out.")
    return redirect("account:login")


def index(request):
    has_accounts = Account.objects.exists()
    current_account = get_current_account(request)
    if has_accounts and current_account is None:
        return redirect("account:login")

    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully.")
            return redirect("account:index")
    else:
        form = AccountForm()

    return render(
        request,
        "account/index.html",
        {
            "title": "Account",
            "description": "Create student and teacher login records used across the system.",
            "form": form,
            "records": Account.objects.order_by("username"),
            "current_account": current_account,
        },
    )
