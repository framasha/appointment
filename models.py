from datetime import datetime
from email.policy import default
from main import db

class Usertype(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    session_duration = db.Column(db.String(10), nullable=True)
    usertype_id = db.Column(db.Integer, db.ForeignKey('usertype.id'), nullable=False)
    usertype = db.relationship('Usertype', backref=db.backref('usertype', lazy=True))

    def __repr__(self):
        return self.email
    
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    coach_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    coach = db.relationship('User', foreign_keys=[coach_id], backref=db.backref('coach', lazy=True))
    client = db.relationship('User', foreign_keys=[client_id], backref=db.backref('client', lazy=True))

    def __repr__(self):
        return self.title

db.create_all()