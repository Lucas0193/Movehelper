from flask import flash, redirect, url_for, render_template, Blueprint

from movehelper.forms.auth import RegisterForm
from movehelper.models import UserAccount, UserTasks
from movehelper.tools import db

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    tasks = UserTasks.query.order_by(UserTasks.pubtime.desc()).limit(5).all()
    return render_template('index.html', tasks=tasks)
    
    