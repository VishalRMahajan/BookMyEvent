from flask_login import LoginManager
from app import app
from modules.users.models import Student, Teacher

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_student(email):
    return Student.query.get(email)