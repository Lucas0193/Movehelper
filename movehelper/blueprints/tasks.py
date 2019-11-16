from flask import render_template, flash, redirect, url_for, Blueprint, request, current_app
from flask_login import login_user, logout_user, login_required, current_user, login_fresh, confirm_login
from datetime import datetime
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
        flash('Task Created!', 'success')
        return redirect(url_for('user.index'))
    return render_template('tasks/newtask.html', form=form)

    
@tasks_bp.route('task/<int:task_id>/<int:editbool>', methods=['GET', 'POST'])
@login_required
@confirm_required
def taskdet(task_id, editbool):
    task = UserTasks.query.get_or_404(task_id)
    userid = current_user.id
    if editbool == 1 :
        return render_template('tasks/taskdet.html', task=task, userid=userid)
    else :
        userid = 0
        return render_template('tasks/taskdet.html', task=task, userid=userid)

@tasks_bp.route('/mytasks', methods=['GET', 'POST'])
@login_required
@confirm_required
def mytasks():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['MOVEHELPER_TASKS_PER_PAGE']
    pagination = UserTasks.query.filter(UserTasks.user_id==current_user.id).order_by(UserTasks.pubtime.desc()).paginate(page, per_page=per_page)
    usertasks = pagination.items
    
    return render_template('tasks/mytasks.html', pagination=pagination, usertasks=usertasks)

@tasks_bp.route('/task/<int:task_id>/taskedit', methods=['GET', 'POST'])
@login_required
@confirm_required
def taskedit(task_id):
    form = NewTask()
    task = UserTasks.query.get_or_404(task_id)
    if form.validate_on_submit():
        task.title = form.title.data
        task.context = form.context.data
        task.contact = form.contact.data
        task.location = form.location.data
        db.session.commit()
        flash('Task Updated!','success')
        return redirect(url_for('tasks.taskdet', task_id=task.id, editbool=1))
    form.title.data = task.title
    form.context.data = task.context
    form.contact.data = task.contact
    form.location.data = task.location
    return render_template('tasks/taskedit.html', form=form, task=task)

@tasks_bp.route('/task/<int:task_id>/taskdelete', methods=['GET', 'POST'])
@login_required
@confirm_required
def taskdelete(task_id):
    task = UserTasks.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash ('Task Deleted!', 'success')
    return redirect(url_for('tasks.mytasks'))