from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
from wtforms.fields import DateField


class Certification(FlaskForm):
    namef = StringField('First Name', validators=[DataRequired()])
    namem = StringField('Mid Name')
    namel = StringField('Last Name', validators=[DataRequired()])
    birthday = DateField('Birth Day', validators=[DataRequired()])
    gender = StringField('Gender', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    onid = StringField('ONID', validators=[DataRequired()])
    license = StringField('Driver License', validators=[DataRequired()])
    submit = SubmitField('Certificate')
