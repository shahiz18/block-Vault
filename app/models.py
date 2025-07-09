from flask_login import UserMixin
from . import db
from datetime import datetime

class UploadLog(db.Model):
    id        = db.Column(db.Integer, primary_key=True)
    filename  = db.Column(db.String(256), nullable=False)
    enc_key   = db.Column(db.LargeBinary, nullable=False)
    cid       = db.Column(db.String(64))              
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(150),default='user')
