from flask import render_template, url_for, redirect
from app import app
from .forms import AddEvent, AddFest
from .models import Event,Fest
from utils.auth import login_manager
from app import bcrypt, db
from flask_login import login_user, login_required, logout_user

@app.route('/addfest' , methods=['GET', 'POST']) 
@login_required
def addfest():
    form=AddFest()

    if form.validate_on_submit():
        fest_id = form.fest_name.data + form.committee.data
        fest = Fest(fest_id=fest_id, fest_name=form.fest_name.data, committee=form.committee.data, coordinator=form.coordinator.data, description=form.description.data)
        db.session.add(fest)
        db.session.commit()

    print(form.errors)

    return render_template('addfest.html', form=form)