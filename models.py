from app import db
from datetime import datetime

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    level = db.Column(db.Integer, default=5)
    data = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, email, password):
        self.email = email
        self.password = password


