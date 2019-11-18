from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, BooleanField, ValidationError, SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms.fields import DateField

class PasswordChange(FlaskForm):
    pwd = PasswordField('Password', validators=[DataRequired(), Length(8,128), EqualTo('pwd2')])
    pwd2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('PasswordChange')

class Certification(FlaskForm):
    namef = StringField('First Name', validators=[DataRequired()])
    namem = StringField('Mid Name')
    namel = StringField('Last Name', validators=[DataRequired()])
    birthday = DateField('Birth Day', validators=[DataRequired()])
    gender = SelectField('Gender', choices=(("male","male"),("female","female"),("other","other")), validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    onid = StringField('ONID', validators=[DataRequired()])
    license = StringField('Driver License', validators=[DataRequired()])
    submit = SubmitField('Certificate')
