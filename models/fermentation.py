import uuid
from models.database import db

class Fermentation(db.Model):
    __tablename__ = "fermentations"

    id = db.Column(db.String(40), primary_key=True, default=lambda: str(uuid.uuid4()))
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)
    temperature = db.Column(db.Float, nullable=True)
    acidity = db.Column(db.Float, nullable=True)
    ph = db.Column(db.Float, nullable=True)
    notes = db.Column(db.String(500), nullable=True)

    variety_id = db.Column(db.String(36), db.ForeignKey("variety.id"), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "temperature": self.temperature,
            "acidity": self.acidity,
            "ph": self.ph,
            "notes": self.notes
        }