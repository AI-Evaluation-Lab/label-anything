from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    markers = db.Column(db.JSON, nullable=False, default={})
    marker_labels = db.Column(db.JSON, nullable=False, default={})
    masks = db.Column(db.JSON, nullable=False, default={})
    path = db.Column(db.String(255), nullable=False)
    embedding_path = db.Column(db.String(255))
    is_difficult = db.Column(db.Boolean, default=False)
    comments = db.Column(db.String, default="")