from models.db import db
import uuid

class Variety(db.Model):
    __tablename__ = "variety"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False, unique=True)  # nombre de la variedad
    description = db.Column(db.Text)  # descripción o detalles

    grape_receptions = db.relationship(
        "GrapeReception",
        back_populates="variety",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"<Variety {self.name}>"
