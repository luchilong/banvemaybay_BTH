from functools import wraps
from flask import redirect
from flask_login import current_user
from mainmb.db_models import user_role

def login_required(f):
    @wraps(f)
    def check(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect('login')

        return f(*args, **kwargs)

    return check


def admin_required(f):
    @wraps(f)
    def check(*args, **kwargs):
        if not current_user.is_authenticated and current_user.Loaiacc == user_role.ADMIN:
            return f(*args, **kwargs)
        else:
            return redirect('/admin')

    return check