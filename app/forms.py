from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
import sqlalchemy as sa
from app import db
from app.models import User
# ...

class CreateUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Register')

class CreateTeamForm(FlaskForm):
    name = StringField('Team Name', validators=[DataRequired()])
    abbreviation = StringField('Team Abbreviation', validators=[DataRequired()])
    logo_link = StringField('Team Logo Link', validators=[DataRequired()])
    submit = SubmitField('Create Team')