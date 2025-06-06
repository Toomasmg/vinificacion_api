import uuid
from models.db import db
from models.variety import Variety

class GrapeReception(db.Model):
    __tablename__ = 'grape_reception'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    grape_type = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    reception_date = db.Column(db.Date, nullable=False)
    image_path = db.Column(db.String(200))  # NUEVO CAMPO

    variety_id = db.Column(db.String(36), db.ForeignKey("variety.id"))
    variety = db.relationship("Variety", back_populates="grape_receptions")

    def __repr__(self):
        return f"<GrapeReception {self.id} - {self.name} - {self.grape_type}>"
