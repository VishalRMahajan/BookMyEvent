import random
from flask import render_template, url_for, redirect,abort
from app import app
from .forms import AddEvent
from .models import Event
from modules.users.models import Student, Committee
from utils.auth import login_manager
from app import bcrypt, db
from flask_login import current_user, login_user, login_required, logout_user



@app.route('/addevent' , methods=['GET', 'POST']) 
@login_required
def addevent():
    if current_user.role != 'Committee':
        abort(403)
    form=AddEvent()

    if form.validate_on_submit():
        event = Event(
            event_name=form.event_name.data, 
            committee=form.committee.data, 
            fest=form.fest.data,
            contact_person=form.contact_person.data,
            description=form.description.data,
            date_added=form.date_added.data,
            event_datetime=form.event_datetime.data,
            ticket_price=form.ticket_price.data,
            venue=form.venue.data,
            phone_number=form.phone_number.data
        )
        db.session.add(event)
        db.session.commit()
        return redirect(url_for('dashboard'))

    print(form.errors)

    return render_template('addevent.html', form=form)