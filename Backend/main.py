from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt



app = Flask(__name__, template_folder='../Frontend/html' ,  static_folder='../Frontend/css')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../databases/database.db'
app.config['SECRET_KEY']= 'secretkey'
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_student(email):
    return Student.query.get(email)


class Student(db.Model, UserMixin):
    pid = db.Column(db.Integer, nullable=False, unique=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name= db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False, primary_key=True)
    password = db.Column(db.String(80), nullable=False)

    def get_id(self):
        return (self.email)

class Teacher(db.Model, UserMixin):
    first_name = db.Column(db.String(20), nullable=False)
    last_name= db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False , primary_key=True)
    password = db.Column(db.String(80), nullable=False)

    def get_id(self):
        return (self.email)

class RegisterStudent(FlaskForm):
    pid = StringField('pid', validators=[InputRequired(), Length(min=6, max=6)], render_kw={"placeholder": "Enter your PID"})
    first_name = StringField('first_name', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Enter your First Name"})
    last_name = StringField('last_name', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Enter your Last Name"})
    email = StringField('email', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Enter your Email"})
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Enter your Password"})
    confirm_password = PasswordField('confirmpassword', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Confirm Password"})
    submit = SubmitField('Register')

    def validate_email(self, email):
        exisiting_email_student = Student.query.filter_by(email=email.data).first()

        if exisiting_email_student:
            raise ValidationError('Email already exists. Please Login')
    
    def validate_pid(self, pid):
        exisiting_pid_student = Student.query.filter_by(pid=pid.data).first()

        if exisiting_pid_student:
            raise ValidationError('Pid already exists. Please Login')
        
    def validate_password(self, password):
        if self.password.data != self.confirm_password.data:
            raise ValidationError('Passwords do not match')
        
        
class loginStudent(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Enter your Email"})
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Enter your Password"})
    submit = SubmitField('login')

    def validate_email(self, email):
        existing_student = Student.query.filter_by(email=email.data).first()
        
        if existing_student is None:
             raise ValidationError('Email does not exist. Please Register')
        else:
            if bcrypt.check_password_hash(existing_student.password, self.password.data) is False:
                raise ValidationError('Password is incorrect. Please try again')
        
    
        




@app.route('/')
def home():
    return render_template('index.html')




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


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

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

if __name__ == '__main__':
    app.run(debug=True)