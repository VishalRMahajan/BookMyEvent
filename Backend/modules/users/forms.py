from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from .models import Student
from app import bcrypt

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