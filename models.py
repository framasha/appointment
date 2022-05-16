from datetime import datetime
from email.policy import default
from main import db

class Coach(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    session_duration = db.Column(db.String(10), nullable=True)
    working_start_time = db.Column(db.Time, nullable=False)
    working_end_time = db.Column(db.Time, nullable=False)

    def __repr__(self):
        return self.email
    
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    coach_id = db.Column(db.Integer, db.ForeignKey('coach.id'), nullable=False)
    coach = db.relationship('Coach', backref=db.backref('coach', lazy=True))

    def __repr__(self):
        return self.title

db.create_all()