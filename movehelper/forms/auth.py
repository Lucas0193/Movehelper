from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, PasswordField, BooleanField

from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo

from wtforms import ValidationError

from movehelper.models import UserAccount

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 254), Email()])
    pwd = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Log in')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20), Regexp('^[a-zA-Z0-9]*$', message='The username should contain only a-z, A-Z and 0-9.')])
    email = StringField('Email', validators=[DataRequired(), Length(1,64), Email()])
    pwd = PasswordField('Password', validators=[DataRequired(), Length(8,128), EqualTo('pwd2')])
    pwd2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')
    def validate_email(self, field):
        if UserAccount.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('The email is already in use.')

    def validate_username(self, field):
        if UserAccount.query.filter_by(username=field.data).first():
            raise ValidationError('The username is already in use.')

