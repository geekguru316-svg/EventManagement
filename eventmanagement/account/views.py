from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .auth import get_current_account
from .forms import AccountForm, AccountUpdateForm, LoginForm, SignupForm
from .models import Account


def redirect_to_role_dashboard(account):
    if account.type == "S":
        return redirect("student:dashboard")
    if account.type == "T":
        return redirect("teacher:dashboard")
    return redirect("home")


def ensure_admin_account(request):
    current_account = get_current_account(request)
    if current_account is None:
        return None, redirect("account:login")
    if current_account.type != "A":
        messages.error(request, "Admin access only.")
        return current_account, redirect_to_role_dashboard(current_account)
    return current_account, None


def login_view(request):
    if not Account.objects.exists():
        messages.info(request, "Create the first account to enable login.")
        return redirect("account:index")

    current = get_current_account(request)
    if current:
        return redirect_to_role_dashboard(current)

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            account = Account.objects.filter(username=username).first()
            if account and account.verify_password(password):
                request.session["account_id"] = account.id
                messages.success(request, f"Welcome, {account.firstname}.")
                return redirect_to_role_dashboard(account)
            messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()

    return render(request, "account/login.html", {"form": form})


def signup_view(request):
    current = get_current_account(request)
    if current:
        return redirect_to_role_dashboard(current)

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            account = form.save()
            request.session["account_id"] = account.id
            messages.success(request, "Account created successfully.")
            return redirect_to_role_dashboard(account)
    else:
        form = SignupForm()

    return render(request, "account/signup.html", {"form": form})


def logout_view(request):
    request.session.pop("account_id", None)
    messages.success(request, "You have been logged out.")
    return redirect("account:login")


def index(request):
    has_accounts = Account.objects.exists()
    current_account = get_current_account(request)
    if has_accounts and current_account is None:
        return redirect("account:login")
    if current_account and current_account.type != "A":
        messages.error(request, "Admin access only.")
        return redirect_to_role_dashboard(current_account)

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
            "description": "Create and manage login records used across the system.",
            "form": form,
            "edit_form": None,
            "edit_account": None,
            "records": Account.objects.order_by("username"),
            "current_account": current_account,
        },
    )


def edit_view(request, account_id):
    current_account, redirect_response = ensure_admin_account(request)
    if redirect_response:
        return redirect_response

    account = get_object_or_404(Account, pk=account_id)
    if request.method == "POST":
        edit_form = AccountUpdateForm(request.POST, instance=account)
        if edit_form.is_valid():
            edit_form.save()
            messages.success(request, "Account updated successfully.")
            return redirect("account:index")
        messages.error(request, "Please correct the form errors below.")
    else:
        edit_form = AccountUpdateForm(instance=account)

    return render(
        request,
        "account/index.html",
        {
            "title": "Account",
            "description": "Create and manage login records used across the system.",
            "form": AccountForm(),
            "edit_form": edit_form,
            "edit_account": account,
            "records": Account.objects.order_by("username"),
            "current_account": current_account,
        },
    )


def delete_view(request, account_id):
    current_account, redirect_response = ensure_admin_account(request)
    if redirect_response:
        return redirect_response
    if request.method != "POST":
        return redirect("account:index")

    account = get_object_or_404(Account, pk=account_id)
    if account.pk == current_account.pk:
        messages.error(request, "You cannot delete your own admin account while logged in.")
        return redirect("account:index")
    if account.type == "A" and Account.objects.filter(type="A").count() <= 1:
        messages.error(request, "Cannot delete the last admin account.")
        return redirect("account:index")

    account.delete()
    messages.success(request, "Account deleted successfully.")
    return redirect("account:index")
