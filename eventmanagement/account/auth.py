from functools import wraps

from django.shortcuts import redirect

from .models import Account


def get_current_account(request):
    account_id = request.session.get("account_id")
    if not account_id:
        return None
    return Account.objects.filter(id=account_id).first()


def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        account = get_current_account(request)
        if account is None:
            return redirect("account:login")
        request.account = account
        return view_func(request, *args, **kwargs)

    return wrapper
