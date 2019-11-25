from flask import flash, redirect, url_for, render_template, Blueprint, request, current_app
from flask_login import login_user, logout_user, login_required, current_user, login_fresh
from sqlalchemy import or_


from movehelper.forms.user import Certification, PasswordChange
from movehelper.models import UserAccount, UserTasks, TaskOrders
from movehelper.tools import db
from movehelper.filter import confirm_required, certificate_required


user_bp = Blueprint('user', '__name__')


@user_bp.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['MOVEHELPER_TASKS_PER_PAGE']
    pagination = UserTasks.query.filter(UserTasks.user_id!=current_user.id).order_by(UserTasks.pubtime.desc()).paginate(page, per_page=per_page)
    tasks = pagination.items
    return render_template('user/index.html', pagination=pagination, tasks=tasks)


@user_bp.route('/passwordchange', methods=['GET', 'POST'])
@login_required
def passwordchange():
    form = PasswordChange()
    if form.validate_on_submit():
        current_user.create_password(form.pwd.data)
        db.session.commit()
        flash('PasswordChange successed. Please re-Login', 'success')
        logout_user()
        return redirect(url_for('main.index'))
    return render_template('user/passwordchange.html', form=form)


@user_bp.route('/certificate', methods=['GET', 'POST'])
@login_required
@confirm_required
def certificate():
    user = UserAccount.query.get_or_404(current_user.id)
    if user.certificated == True :
        flash('You were already certificated!', 'warning')
        return redirect(url_for('user.index'))
    else :
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
            current_user.certificated = True
            db.session.commit()
            flash('Certification successed.', 'success')
            return redirect(url_for('user.index'))
        return render_template('user/certificate.html', form = form)


@user_bp.route('/applytask/<int:task_id>', methods=['GET', 'POST'])
@login_required
@confirm_required
@certificate_required
def applytask(task_id):
    task = UserTasks.query.get_or_404(task_id)
    if  task.status == False:
        if task.mpnume < (task.mpnum - 1): 
            neworder = TaskOrders(manpower=current_user.id, task_id=task_id)
            task.mpnume += 1
            db.session.add(neworder)
            db.session.commit()
            flash('You applied this task', 'success')
            return redirect(url_for('user.index'))
        else:
            neworder = TaskOrders(manpower=current_user.id, task_id=task_id)
            task.mpnume += 1
            task.status = True
            db.session.add(neworder)
            db.session.commit()
            flash('You applied this task', 'success')
            return redirect(url_for('user.index'))
    else :  
        flash('This task was closed', 'warning')
        return redirect(url_for('tasks.taskdet', task_id=task.id))


@user_bp.route('/myapply', methods=['GET', 'POST'])
@login_required
@confirm_required
@certificate_required
def myapply():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['MOVEHELPER_TASKS_PER_PAGE']
    pagination = UserTasks.query.join(TaskOrders).filter(TaskOrders.manpower==current_user.id).with_entities(TaskOrders.id, TaskOrders.task_id, UserTasks.title, TaskOrders.createtime).order_by(TaskOrders.createtime.desc()).paginate(page, per_page=per_page)
    applys = pagination.items
    return render_template('user/myapplys.html', pagination=pagination, applys=applys)