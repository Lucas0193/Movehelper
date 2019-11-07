from flask import render_template, flash, redirect, url_for, Blueprint, request, current_app
from flask_login import login_user, logout_user, login_required, current_user, login_fresh, confirm_login

from movehelper.config import Operations
from movehelper.emails import send_confirm_email
from movehelper.forms.tasks import NewTask
from movehelper.models import UserAccount, UserTasks
from movehelper.tools import db
from movehelper.helpers import generate_token, validate_token
from movehelper.filter import confirm_required

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/new', methods=['GET', 'POST'])
@login_required
@confirm_required
def newtask():
    form = NewTask()
    if form.validate_on_submit():
        title = form.title.data
        context = form.context.data
        contact = form.contact.data
        location = form.location.data
        task = UserTasks(title=title, context=context, contact=contact, location=location, user_id=current_user.id )
        db.session.add(task)
        db.session.commit()
        flash('Task Created', 'success')
        return redirect(url_for('user.index'))
    return render_template('tasks/newtask.html', form=form)

    
@tasks_bp.route('/<int:task_id>', methods=['GET', 'POST'])
@login_required
@confirm_required
def taskdet(task_id):
    task = UserTasks.query.get_or_404(task_id)
    
    return render_template('tasks/taskdet.html', task=task)

@tasks_bp.route('/mytasks', methods=['GET', 'POST'])
@login_required
@confirm_required
def mytasks():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['MOVEHELPER_TASKS_PER_PAGE']
    pagination = UserTasks.query.filter(UserTasks.user_id==current_user.id).order_by(UserTasks.pubtime.desc()).paginate(page, per_page=per_page)
    usertasks = pagination.items
    
    return render_template('tasks/mytasks.html', pagination=pagination, usertasks=usertasks)