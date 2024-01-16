from app import app, db
from utils import auth
from modules.users import views
from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user
from modules.users.models import Student
from modules.users.forms import loginStudent, RegisterStudent

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    current_student = current_user
    return render_template('dashboard.html', first_name=current_student.first_name, last_name=current_student.last_name, email=current_student.email)


@app.route('/profile')
@login_required
def profile():
    student = current_user
    return render_template('profile.html', first_name=student.first_name, last_name=student.last_name, email=student.email, pid=student.pid)

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
    app.run(debug=True)
