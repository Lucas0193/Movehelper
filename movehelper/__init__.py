import os


import click
from flask import Flask, render_template,request
from faker import Faker


from movehelper.blueprints.user import user_bp
from movehelper.blueprints.main import main_bp
from movehelper.blueprints.auth import auth_bp
from movehelper.blueprints.tasks import tasks_bp
from movehelper.tools import db, bootstrap, loginmanager, mail
from movehelper.config import config
from movehelper.models import UserAccount, UserTasks, TaskOrders


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

    @app.cli.command()
    @click.option('--count', default=6, help='Quantity of UserAccount, default is 6.')
    def forgeusercer(count):
        """Generate fake users"""

        fake = Faker() 
        click.echo('Working...')

        id = 100000
        pwd = 'testpassword'
        for i in range(count):
            id = id + 1
            user = UserAccount(
                id=id,
                username=fake.name(),
                email=fake.email(),
                fname=fake.first_name(),
                lname=fake.last_name(),
                birth=fake.date_of_birth(),
                gender='male',
                phone=fake.phone_number(),
                onid=fake.ean(length=8),
                license=fake.invalid_ssn(),
                confirmed=True,
                certificated=True
            )
            user.create_password(pwd)
            db.session.add(user)

        db.session.commit()

        click.echo(f'Created {count} fake users!')

    @app.cli.command()
    @click.option('--count', default=3, help='Quantity of UserAccount, default is 3.')
    def forgeusercon(count):
        """Generate fake users"""

        fake = Faker() 
        click.echo('Working...')

        id = 100006
        pwd = 'testpassword'
        for i in range(count):
            id = id + 1
            user = UserAccount(
                id=id,
                username=fake.name(),
                email=fake.email(),
                confirmed=True,
                certificated=False
            )
            user.create_password(pwd)
            db.session.add(user)

        db.session.commit()

        click.echo(f'Created {count} fake users!')

    @app.cli.command()
    @click.option('--count', default=1, help='Quantity of UserAccount, default is 1.')
    def forgeuseruncon(count):
        """Generate fake users"""

        fake = Faker() 
        click.echo('Working...')

        id = 100009
        pwd = 'testpassword'
        for i in range(count):
            id = id + 1
            user = UserAccount(
                id=id,
                username=fake.name(),
                email=fake.email(),
                confirmed=False,
                certificated=False
            )
            user.create_password(pwd)
            db.session.add(user)

        db.session.commit()

        click.echo(f'Created {count} fake users!')


    @app.cli.command()
    @click.option('--count', default=9, help='Quantity of UserTasks, default is 9.')
    def forgetasks(count):
        """Generate fake users"""

        fake = Faker() 
        click.echo('Working...')
        
        id = 100000
        for i in range(count):
            id = id + 1
            task = UserTasks(
                pubtime=fake.date_time_this_year(),
                title=fake.sentence(),
                context=fake.text(),
                contact=fake.phone_number(),
                location=fake.address(),
                mpnum=1 + int(i/3),
                user_id=id
            )
            db.session.add(task)

        db.session.commit()

        click.echo(f'Created {count} fake tasks!')