from models.db import db
import uuid
from datetime import date

class GrapeVariety(db.Model):
    __tablename__ = 'grape_varieties'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)

    def __init__(self, name):
        self.name = name

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }