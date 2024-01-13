from flask import render_template, url_for, redirect
from app import app
from .forms import loginStudent, RegisterStudent
from .models import Student
from utils.auth import login_manager
from app import bcrypt, db
from flask_login import login_user, login_required, logout_user

@app.route('/login', methods=['GET', 'POST'])
def login():
    form=loginStudent()

    if form.validate_on_submit():
        student= Student.query.filter_by(email=form.email.data).first()
        if student:
            if bcrypt.check_password_hash(student.password, form.password.data):
                login_user(student)
                return redirect(url_for('dashboard')) 

    print(form.errors)

    return render_template('login.html', form=form)

@app.route('/register' , methods=['GET', 'POST']) 
def register():
    form=RegisterStudent()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        student = Student(pid=form.pid.data, first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, password=hashed_password)
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('login'))

    print(form.errors)

    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))