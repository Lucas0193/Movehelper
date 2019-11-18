from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, ValidationError, HiddenField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, Optional, URL

from movehelper.models import UserTasks


class NewTask(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 60)])
    context = CKEditorField('Context', validators=[DataRequired()])
    contact = StringField('Contact', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    manpower = SelectField('Manpower Requirement', choices=(("1","1"),("2","2"),("3","3")), validators=[DataRequired()])
    submit = SubmitField()