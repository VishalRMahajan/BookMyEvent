from flask import flash, render_template, request, session, url_for, redirect
from app import app
from .forms import loginStudent, RegisterStudent, Otp, AddCommittee
from .models import Student, Coordinator, Committee
from utils.auth import login_manager
from app import bcrypt, db
from flask_login import login_user, login_required, logout_user
import pyotp
from modules.email.views import send_otp

@app.route('/login', methods=['GET', 'POST'])
def login():
    form=loginStudent()
    session['role']= form.role.data
    if form.validate_on_submit():
        if form.role.data == 'User':
            student= Student.query.filter_by(email=form.email.data).first()
            if student:
                if bcrypt.check_password_hash(student.password, form.password.data):
                    login_user(student)
                    return redirect(url_for('dashboard')) 
        elif form.role.data == 'Coordinator':
            coordinator= Coordinator.query.filter_by(email=form.email.data).first()
            if coordinator:
                if bcrypt.check_password_hash(coordinator.password, form.password.data):
                    login_user(coordinator)
                    return redirect(url_for('dashboard'))
        elif form.role.data == 'Committee':
            committee= Committee.query.filter_by(email=form.email.data).first()
            if committee:
                if bcrypt.check_password_hash(committee.password, form.password.data):
                    login_user(committee)
                    return redirect(url_for('dashboard'))

    print(form.errors)

    return render_template('login.html', form=form)

@app.route('/register' , methods=['GET', 'POST']) 
def register():
    form=RegisterStudent()

    if form.validate_on_submit():
        session['email'] = form.email.data
        session['role']= form.role.data
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        if form.role.data == 'User':
            user = Student(pid=form.pid.data, first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, password=hashed_password, is_active=False)
        elif form.role.data == 'Coordinator':
            user = Coordinator(role=form.role.data,committee=form.committee.data, first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, password=hashed_password, is_active=False)
        elif form.role.data == 'Committee':
            user = Committee(role=form.role.data,committee=form.committee.data, first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, password=hashed_password, is_active=False)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('otp_verification'))

    print(form.errors)

    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/register/otp', methods=['GET', 'POST'])
def otp_verification():
    if 'email' not in session:
        return redirect(url_for('register'))
    email = session['email']
    totp = pyotp.TOTP('base32secret3232')
    form = Otp()
    if 'otp' not in session:
        otp = totp.now()
        session['otp'] = otp
        send_otp(email, otp)
    if form.validate_on_submit():
        if form.otp.data == session['otp']:
            role = session['role']
            if role == 'User':
                user = Student.query.filter_by(email=email).first()
            elif role == 'Coordinator':
                user = Coordinator.query.filter_by(email=email).first()
            elif role == 'Committee':
                user = Committee.query.filter_by(email=email).first()
            # Update the is_active attribute
            user.is_active = True
            # Commit the changes to the database
            db.session.commit()
            session.pop('email', None)
            session.pop('otp', None)
            return redirect(url_for('login'))
    return render_template("otp.html", form=form)

@app.route('/login/otp', methods=['GET', 'POST'])
def verify_email():
    email = request.args.get('email')
    role = session['role']
    user = None
    if role == 'User':
        user = Student.query.filter_by(email=email).first()
    elif role == 'Coordinator':
        user = Coordinator.query.filter_by(email=email).first()
    elif role == 'Committee':
        user = Committee.query.filter_by(email=email).first()
    if not user:
        flash('No user found with this email', 'error')
        return redirect(url_for('login'))

    totp = pyotp.TOTP('base32secret3232')
    form = Otp()
    if 'otp' not in session:
        otp = totp.now()
        session['otp'] = otp
        send_otp(email, otp)
    if form.validate_on_submit():
        if form.otp.data == session['otp']:
            if user:
                user.is_active = True
                db.session.commit()
            session.pop('otp', None)
            return redirect(url_for('login'))
    return render_template("otp.html", form=form)

