from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, PasswordField, SubmitField,TextAreaField
from wtforms.validators import InputRequired, Length, ValidationError
from .models import Fest, Event
from app import bcrypt

class AddFest(FlaskForm):
    fest_id = StringField('fid', validators=[InputRequired(), Length(min=6, max=6)], render_kw={"placeholder": "Enter your PID"})
    fest_name = StringField('fest_name', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Enter Fest Name"})
    committee = SelectField('Committee', choices=[('ITSA', 'ITSA'), ('ISTE', 'ISTE'), ('CSI', 'CSI')], validators=[InputRequired()])
    coordinator = StringField('coordinator', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Enter Coordinator"})
    description = TextAreaField('Description', validators=[InputRequired(), Length(min=4, max=200)], render_kw={"placeholder": "Enter Description"})
    submit = SubmitField('Add Fest')

class AddEvent(FlaskForm):
    event_id = StringField('eid', validators=[InputRequired(), Length(min=6, max=6)], render_kw={"placeholder": "Enter your PID"})
    event_name = StringField('event_name', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Enter Event Name"})
    committee = SelectField('Committee', choices=[('ITSA', 'ITSA'), ('ISTE', 'ISTE'), ('CSI', 'CSI')], validators=[InputRequired()])
    coordinator = StringField('cooridnator', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Enter Coordinator"})
    description = TextAreaField('Description', validators=[InputRequired(), Length(min=4, max=200)], render_kw={"placeholder": "Enter Description"})
    submit = SubmitField('Add Event')