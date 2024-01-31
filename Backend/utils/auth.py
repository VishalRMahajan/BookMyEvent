from flask_login import LoginManager
from app import app
from modules.users.models import Student, Coordinator,Committee

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(role):
    user = Student.query.filter_by(role=role).first()
    if user is None:
        user = Coordinator.query.filter_by(role=role).first()
    if user is None:
        user = Committee.query.filter_by(role=role).first()
    
    return user