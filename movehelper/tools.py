
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail



db = SQLAlchemy()
bootstrap = Bootstrap()
loginmanager = LoginManager()
mail = Mail()

@loginmanager.user_loader
def load_user(user_id):
    from movehelper.models import UserAccount
    user = UserAccount.query.get(int(user_id))
    return user