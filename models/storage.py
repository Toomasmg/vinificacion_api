from models.db import db
import uuid
from models.variety import Variety
from datetime import date
class Storage(db.Model):
    __tablename__ = 'storages'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    wine_name = db.Column(db.String(100), nullable=False)

    grape_variety_id = db.Column(db.String(36), db.ForeignKey('variety.id'), nullable=False)
    grape_variety = db.relationship("Variety", backref="storages")

    container_type = db.Column(db.String(50), nullable=False)
    quantity_liters = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(100), nullable=True)

    def __init__(self, wine_name, grape_variety_id, container_type, quantity_liters, location=None):
        self.wine_name = wine_name
        self.grape_variety_id = grape_variety_id
        self.container_type = container_type
        self.quantity_liters = quantity_liters
        self.location = location

    def serialize(self):
        return {
            'id': self.id,
            'wine_name': self.wine_name,
            'grape_variety_id': self.grape_variety_id,
            'container_type': self.container_type,
            'quantity_liters': self.quantity_liters,
            'location': self.location
        }
