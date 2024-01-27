from datetime import datetime
import os
from flask import current_app
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import DateField, DateTimeLocalField, FileField, IntegerField, SelectField, StringField, SubmitField,TextAreaField
from wtforms.validators import InputRequired, Length, NumberRange
from .models import  Event
from app import bcrypt



class AddEvent(FlaskForm):
    event_name = StringField('event_name', validators=[InputRequired(), Length(min=2, max=25)], render_kw={"placeholder": "Event Name"})
    committee = SelectField('Committee', choices=[('none', '-- Choose Committee --'),('StudentCouncil', 'Student Council'),('ITSA', 'ITSA'), ('ISTE', 'ISTE'), ('CSI', 'CSI')], validators=[InputRequired()])
    fest = SelectField('Committee', choices=[('none', '-- Choose Fest --'), ('Mosaic', 'Mosaic'), ('iris', 'Iris'),('Ignitra', 'Ignitra'),('Other', 'Other')], validators=[InputRequired()])
    contact_person = StringField('cooridnator', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Contact Person"})
    description = TextAreaField('Description', validators=[InputRequired(), Length(min=4, max=200)], render_kw={"placeholder": "Details about the event"})
    date_added = DateField('DateAdded', default=datetime.today)
    event_datetime = DateTimeLocalField('EventDateTime', format='%Y-%m-%dT%H:%M', validators=[InputRequired()])
    ticket_price = IntegerField('TicketPrice', validators=[InputRequired(), NumberRange(min=0, max=10000)], render_kw={"placeholder": "Price (Enter 0 if free)"})
    venue = StringField('Venue', validators=[InputRequired(), Length(max=50)], render_kw={"placeholder": "Venue"})
    phone_number = IntegerField('PhoneNumber', validators=[InputRequired()], render_kw={"placeholder": "Contact Person's Phone Number"})
    image_file = FileField('Event Image', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Add Event')

    