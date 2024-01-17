from app import db

class Fest(db.Model):
    fest_id = db.Column(db.Integer, primary_key=True)
    fest_name = db.Column(db.String(20), nullable=False)
    committee = db.Column(db.String(20), nullable=False)
    coordinator = db.Column(db.String(20), nullable=True)
    description = db.Column(db.String(200), nullable=False)

    def get_id(self):
        return self.fest_id
    
class Event(db.Model):
    event_id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(20), nullable=False)
    committee = db.Column(db.String(20), nullable=False)
    coordinator = db.Column(db.String(20), nullable=True)
    description = db.Column(db.String(200), nullable=False)
    fest_id = db.Column(db.Integer, db.ForeignKey('fest.fest_id'), nullable=True)

    fest = db.relationship('Fest', backref=db.backref('events', lazy=True))

    def get_id(self):
        return self.event_id