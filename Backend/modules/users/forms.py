from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from .models import Student, Committee
from app import bcrypt

class RegisterStudent(FlaskForm):
    pid = StringField('pid', validators=[InputRequired(), Length(min=6, max=6)], render_kw={"placeholder": "Enter your PID"})
    role = SelectField('Committee', choices=[('User', 'User'), ('Committee', 'Committe')], validators=[InputRequired()])
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
        elif self.role.data == 'Committee':
            existing_user = Committee.query.filter_by(email=email.data).first()

        if existing_user:
            raise ValidationError('Email already exists. Please Login')
        

    def validate_pid(self, pid):
        exisiting_pid_student = None
        if self.role.data == 'User':
            exisiting_pid_student = Student.query.filter_by(pid=pid.data).first()
        elif self.role.data == 'Committee':
            exisiting_pid_student = Committee.query.filter_by(pid=pid.data).first()

        if exisiting_pid_student:
            raise ValidationError('Pid already exists. Please Login')
        
    def validate_password(self, password):
        if self.password.data != self.confirm_password.data:
            raise ValidationError('Passwords do not match')
        
        
class loginStudent(FlaskForm):
    role = SelectField('Committee', choices=[('User', 'User'), ('Committee', 'Committe')], validators=[InputRequired()])
    email = StringField('email', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Enter your Email"})
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Enter your Password"})
    submit = SubmitField('login')

    def validate_email(self, email):
        user = None
        if self.role.data == 'User':
            user = Student.query.filter_by(email=email.data).first()
        elif self.role.data == 'Committee':
            user = Committee.query.filter_by(email=email.data).first()

        if user is None:
            raise ValidationError('Email does not exist. Please Register')
        else:
            if bcrypt.check_password_hash(user.password, self.password.data) is False:
                raise ValidationError('Password is incorrect. Please try again')