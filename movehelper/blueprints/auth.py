from flask import render_template, flash, redirect, url_for, Blueprint
from flask_login import login_user, logout_user, login_required, current_user, login_fresh, confirm_login

from movehelper.config import Operations
from movehelper.emails import send_confirm_email
from movehelper.forms.auth import RegisterForm, LoginForm
from movehelper.models import UserAccount
from movehelper.tools import db
from movehelper.helpers import generate_token, validate_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = UserAccount.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.verify_password(form.pwd.data):
            if login_user(user, form.remember_me.data):
                flash('Login success.', 'info')
                return redirect(url_for('user.index'))
            else:
                flash('Your account is blocked.', 'warning')
                return redirect(url_for('main.index'))
        flash('Invalid email or password.', 'warning')
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout success!','info')
    return redirect(url_for('main.index'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('user.index'))
    lastuser = UserAccount.query.order_by(UserAccount.id.desc()).first()
    if lastuser != None:
        id = int(lastuser.id)
    else:
        id = 100000
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data.lower()
        pwd = form.pwd.data
        newid = id + 1
        user = UserAccount(id=newid, username=username, email=email)
        user.create_password(pwd)
        db.session.add(user)
        db.session.commit()
        token = generate_token(user=user, operation='confirm')
        send_confirm_email(user=user, token=token)
        flash('Confirm email sent, check your inbox.', 'info')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)

@auth_bp.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        flash('You are already comfirmed')
        return redirect(url_for('user.index'))

    if validate_token(user=current_user, token=token, operation=Operations.CONFIRM):
        flash('Account confirmed.', 'success')
        return redirect(url_for('user.index'))
    else:
        flash('Invalid or expired token.', 'danger')
        return redirect(url_for('.resend_confirm_email'))


@auth_bp.route('/resend-confirm-email')
@login_required
def resend_confirm_email():
    if current_user.confirmed:
        return redirect(url_for('user.index'))

    token = generate_token(user=current_user, operation=Operations.CONFIRM)
    send_confirm_email(user=current_user, token=token)
    flash('New email sent, check your inbox.', 'info')
    return redirect(url_for('user.index'))