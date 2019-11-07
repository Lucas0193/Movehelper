from flask import flash, redirect, url_for, render_template, Blueprint, request, current_app
from flask_login import login_user, logout_user, login_required, current_user, login_fresh

from movehelper.forms.user import Certification
from movehelper.models import UserAccount, UserTasks
from movehelper.tools import db
from movehelper.filter import confirm_required

user_bp = Blueprint('user', '__name__')

@user_bp.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['MOVEHELPER_TASKS_PER_PAGE']
    pagination = UserTasks.query.order_by(UserTasks.pubtime.desc()).paginate(page, per_page=per_page)
    tasks = pagination.items
    return render_template('user/index.html', pagination=pagination, tasks=tasks)

@user_bp.route('/certificate', methods=['GET', 'POST'])
@login_required
@confirm_required
def certificate():
    form = Certification()
    if form.validate_on_submit():
        current_user.fname = form.namef.data
        current_user.mname = form.namem.data
        current_user.lname = form.namel.data
        current_user.birth = form.birthday.data
        current_user.gender = form.gender.data
        current_user.phone = form.phone.data
        current_user.onid = form.onid.data
        current_user.license = form.license.data
        db.session.commit()
        flash('edit successed.', 'success')
        return redirect(url_for('user.index'))
    return render_template('user/certificate.html', form = form)
