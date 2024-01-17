from app import app, db
from utils import auth
from modules.users import views
from modules.fest import views
from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user
from modules.fest.models import Event
from modules.users.models import Student,Committee
from modules.users.forms import loginStudent, RegisterStudent
from datetime import datetime

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    today = datetime.today()
    in_progress_events = Event.query.filter(Event.event_datetime >= today).all()
    return render_template('dashboard.html', first_name=current_user.first_name, role=current_user.role, in_progress_events=in_progress_events)


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', first_name=current_user.first_name, last_name=current_user.last_name, email=current_user.email, pid=current_user.pid, role=current_user.role)

@app.route('/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        pid = request.form.get('pid')

        # Assuming you have a Student model with these fields
        student = Student.query.filter_by(pid=pid).first()
        if student:
            student.first_name = first_name
            student.last_name = last_name
            db.session.commit()

    return redirect(url_for('profile'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
