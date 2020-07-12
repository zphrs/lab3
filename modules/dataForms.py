from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField
from wtforms.widgets import PasswordInput
from wtforms.validators import DataRequired
from wtforms.validators import Length


class UserForm(FlaskForm):
    first_name = StringField('First Name', validators=[Length(min=1, max=64)])
    age = IntegerField('Age', validators=[DataRequired()])
    password = StringField('password', widget=PasswordInput(hide_value=False), validators=[DataRequired()])
    submit = SubmitField('Enter')
class passwordConfirmation(FlaskForm):
    password = StringField('password', widget=PasswordInput(hide_value=False), validators=[DataRequired()])
    submit = SubmitField('Enter')
class ChangeForm(FlaskForm):
    first_name = StringField('First Name (optional)')
    age = StringField('Age (optional)')
    password = StringField('password', widget=PasswordInput(hide_value=False), validators=[DataRequired()])
    submit = SubmitField('Enter')
class GenerateForm(FlaskForm):
    numOfUsers = IntegerField('Number of users to generate', validators=[DataRequired()])
    submit = SubmitField('Enter')