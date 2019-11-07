
import os

import click
from flask import Flask, render_template,request

from movehelper.blueprints.user import user_bp
from movehelper.blueprints.main import main_bp
from movehelper.blueprints.auth import auth_bp
from movehelper.blueprints.tasks import tasks_bp
from movehelper.tools import db, bootstrap, loginmanager, mail
from movehelper.config import config
from movehelper.models import UserAccount

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('movehelper')
    app.config.from_object(config[config_name])
    

    register_tools(app)
    register_blueprints(app)
    register_commands(app)
    return app

def register_tools(app):
    db.init_app(app)
    bootstrap.init_app(app)
    loginmanager.init_app(app)
    mail.init_app(app)

def register_blueprints(app):
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(tasks_bp, url_prefix='/tasks')
    app.register_blueprint(main_bp)

def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')