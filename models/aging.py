from models.db import db
import uuid
from models.variety import Variety
from models.bottling import Bottling
from datetime import date

class Aging(db.Model):
    __tablename__ = 'agings'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    grape_variety_id = db.Column(db.String(36), db.ForeignKey('variety.id'), nullable=False)
    grape_variety = db.relationship("Variety", backref="agings")

    barrel_type = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)

    bottlings = db.relationship('Bottling', backref='aging', cascade='all, delete-orphan')

    def __init__(self, grape_variety_id, barrel_type, start_date, end_date=None):
        self.grape_variety_id = grape_variety_id
        self.barrel_type = barrel_type
        self.start_date = start_date
        self.end_date = end_date

    def serialize(self):
        return {
            'id': self.id,
            'grape_variety_id': self.grape_variety_id,
            'barrel_type': self.barrel_type,
            'start_date': str(self.start_date),
            'end_date': str(self.end_date) if self.end_date else None
        }