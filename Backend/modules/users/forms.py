from flask import redirect, session, url_for
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, DataRequired
from .models import Student, Coordinator, Committee
from app import bcrypt

class RegisterStudent(FlaskForm):
    pid = StringField('pid',id="pid", validators=[Length(min=0, max=6)], render_kw={"placeholder": "Enter your PID"})
    role = SelectField('role',id="role", choices=[('User', 'User'), ('Coordinator', 'Coordinator'),('Committee','Committee')], validators=[InputRequired()])
    committee = SelectField('committee', id='committee', choices=[('StudentCouncil', 'Student Council'), ('ITSA', 'ITSA')], validators=[InputRequired()])
    first_name = StringField('first_name', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Enter your First Name"})
    last_name = StringField('last_name', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Enter your Last Name"})
    email = StringField('email', validators=[InputRequired(), Length(min=4, max=30)], render_kw={"placeholder": "Enter your Email"})
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Enter your Password"})
    confirm_password = PasswordField('confirmpassword', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Confirm Password"})
    submit = SubmitField('Register')

    def validate_email(self, email):
        existing_user = None
        if self.role.data == 'User':
            existing_user = Student.query.filter_by(email=email.data).first()
        elif self.role.data == 'Coordinator':
            existing_user = Coordinator.query.filter_by(email=email.data).first()

        if existing_user:
            raise ValidationError('Email already exists. Please Login')
        

    def validate_pid(self, pid):
        if self.role.data == 'User':
            existing_pid_student = Student.query.filter_by(pid=pid.data).first()
            if existing_pid_student:
                raise ValidationError('Pid already exists. Please Login')


        
        
    def validate_password(self, password):
        if self.password.data != self.confirm_password.data:
            raise ValidationError('Passwords do not match')
        
        
class loginStudent(FlaskForm):
    role = SelectField('Role', choices=[('User', 'User'), ('Coordinator', 'Coordinator'),('Committee','Committee')], validators=[InputRequired()])
    email = StringField('email', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Enter your Email"})
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Enter your Password"})
    submit = SubmitField('login')

    
    def validate_email(self, email):
        user = None
        if self.role.data == 'User':
            user = Student.query.filter_by(email=email.data).first()
        elif self.role.data == 'Coordinator':
            user = Coordinator.query.filter_by(email=email.data).first()
        elif self.role.data == 'Committee':
            user = Committee.query.filter_by(email=email.data).first()
            
        if user is None:
            raise ValidationError('Email does not exist. Please Register')
        else:
            if bcrypt.check_password_hash(user.password, self.password.data) is False:
                raise ValidationError('Password is incorrect. Please try again')
            
        if user.is_active is False:
            raise ValidationError('Please verify your email')


class Otp(FlaskForm):
    otp = StringField('otp', validators=[InputRequired(), Length(min=6, max=6)], render_kw={"placeholder": "Enter OTP"})
    
    def validate_otp(self, otp):
        if otp.data != session['otp']:
            raise ValidationError('OTP is incorrect. Please try again')
    submit = SubmitField('Verify OTP')


class AddCommittee(FlaskForm):
    Committee_name = StringField('Committee_name', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Enter the Committee Name"})
    email = StringField('email', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Enter your Email"})
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Enter your Password"})
    coordinator = SelectField('Coordinator', validators=[DataRequired()])
    def __init__(self, *args, **kwargs):
        super(AddCommittee, self).__init__(*args, **kwargs)
        self.coordinator.choices = [(c.email, c.first_name + ' ' + c.last_name) for c in Coordinator.query.order_by(Coordinator.first_name).all()]
    submit = SubmitField('addcommittee')
