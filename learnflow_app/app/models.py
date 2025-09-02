# Database models (User, Session)
from app import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    subscription_status = db.Column(db.String(20), default='free')
    stripe_customer_id = db.Column(db.String(100))
    sessions = db.relationship('Session', backref='user', lazy=True)

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    input_text = db.Column(db.Text, nullable=False)
    ai_feedback = db.Column(db.JSON)  # Stores the AI's JSON response
    confidence_score = db.Column(db.String(20))  # SOLID, PARTIAL, NEEDS_REVIEW
    created_at = db.Column(db.DateTime, default=datetime.utcnow)