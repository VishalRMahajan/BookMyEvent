from app import app
from flask_mail import Mail, Message
import os

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = ''

app.config['MAIL_PASSWORD'] =  ''
mail = Mail(app)


def send_otp(email, otp):
    msg = Message('OTP for your account', sender='', recipients=[email])
    msg.body = f'Your OTP is {otp}'
    
    mail.send(msg)
