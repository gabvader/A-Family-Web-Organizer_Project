from datetime import datetime, date
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectMultipleField, DateField, TimeField, SelectField
from wtforms.fields import Field
from wtforms.widgets import DateTimeLocalInput
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Optional
from app.models import User

class DateTimeLocalField(Field):
    widget = DateTimeLocalInput()

    def __init__(self, label=None, validators=None, format='%Y-%m-%dT%H:%M', **kwargs):
        super(DateTimeLocalField, self).__init__(label, validators, **kwargs)
        self.format = format

    def _value(self):
        if self.raw_data:
            return ' '.join(self.raw_data)
        else:
            return self.data and self.data.strftime(self.format) or ''

    def process_formdata(self, valuelist):
        if valuelist:
            date_str = ' '.join(valuelist)
            try:
                self.data = datetime.strptime(date_str, self.format)
            except ValueError:
                self.data = None
                raise ValueError('Not a valid datetime value')



class LoginForm(FlaskForm):
    identificator = StringField('Email or Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
    
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    alias = StringField('Alias')
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    family_name = StringField('Family Name')
    new_family_name = StringField('New Family Name')
    submit = SubmitField('Register')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
    
class ManageUserDataForm(FlaskForm):
    alias = StringField('Alias')
    email = StringField('Email', validators=[Email()])
    current_password = PasswordField('Current Password', validators=[Optional()])
    new_password = PasswordField('New Password', validators=[Optional()])
    confirm_new_password = PasswordField('Confirm New Password', validators=[Optional(), EqualTo('new_password')])
    submit = SubmitField('Save Changes')

class EventForm(FlaskForm):
    title = StringField('Event Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    start_date = DateField('Start Date', validators=[DataRequired()], format='%Y-%m-%d', default=date.today)
    start_time = TimeField('Start Time', validators=[Optional()], format='%H:%M')
    end_date = DateField('End Date', validators=[Optional()], format='%Y-%m-%d')
    end_time = TimeField('End Time', validators=[Optional()], format='%H:%M')
    participants = SelectMultipleField('Participants', coerce=int)
    event_type = SelectField('Event Type', coerce=int)
    new_event_type = StringField('New Event Type')
    submit = SubmitField('Create Event')
    
class EditEventForm(FlaskForm):
    title = StringField('Event Title')
    description = TextAreaField('Description')
    start_date = DateField('Start Date', validators=[Optional()], format='%Y-%m-%d', default=date.today)
    start_time = TimeField('Start Time', validators=[Optional()], format='%H:%M')
    end_date = DateField('End Date', validators=[Optional()], format='%Y-%m-%d')
    end_time = TimeField('End Time', validators=[Optional()], format='%H:%M')
    participants = SelectMultipleField('Participants', coerce=int)
    event_type = SelectField('Event Type', coerce=int)
    new_event_type = StringField('New Event Type')
    submit = SubmitField('Update Event')
    