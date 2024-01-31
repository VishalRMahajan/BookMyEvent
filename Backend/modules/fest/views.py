import os
import random
from flask import render_template, url_for, redirect,abort
from app import app
from .forms import AddEvent
from .models import Event
from modules.users.models import Student, Committee
from utils.auth import login_manager
from app import bcrypt, db
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.utils import secure_filename
from flask import request



@app.route('/addevent' , methods=['GET', 'POST']) 
@login_required
def addevent():
    if current_user.role == 'User':
        abort(403)
    form=AddEvent()

    if form.validate_on_submit():
        if 'image_file' in request.files:
            image_file = request.files['image_file']
            filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_filename = filename
        else:
            image_filename = None 
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
            phone_number=form.phone_number.data,
            image_file=image_filename
        )
        db.session.add(event)
        db.session.commit()
        return redirect(url_for('dashboard'))

    print(form.errors)

    return render_template('addevent.html', form=form)


@app.route('/event/<event_name>')
@login_required
def festpage(event_name):
    event_name_with_spaces = event_name.replace('-', ' ')
    event = Event.query.filter_by(event_name=event_name_with_spaces).first()
    if event is None:
        abort(404)
    return render_template('festpage.html', event_name=event.event_name, 
            committee=event.committee, 
            fest=event.fest,
            contact_person=event.contact_person,
            description=event.description,
            date_added=event.date_added,
            event_datetime=event.event_datetime,
            ticket_price=event.ticket_price,
            venue=event.venue,
            phone_number=event.phone_number )

@app.route('/myevents')
@login_required
def myevents():
    committee = current_user.committee if hasattr(current_user, 'committee') else None
    events = Event.query.filter_by(committee=committee).all()
    return render_template('myevents.html', events=events)