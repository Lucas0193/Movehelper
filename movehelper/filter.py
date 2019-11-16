from functools import wraps

from flask import Markup, flash, url_for, redirect, abort
from flask_login import current_user


def confirm_required(func):
    @wraps(func)
    def filter_function(*args, **kwargs):
        if not current_user.confirmed:
            message = Markup(
                'Please confirm your account first.'
                'Not receive the email?'
                '<a class="alert-link" href="%s">Resend Confirm Email</a>' %
                url_for('auth.resend_confirm_email'))
            flash(message, 'warning')
            return redirect(url_for('user.index'))
        return func(*args, **kwargs)
    return filter_function