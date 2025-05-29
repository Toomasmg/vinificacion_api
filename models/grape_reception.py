import uuid
from database import db
from models.variety import Variety

# Modelo que representa la recepción de la uva en la bodega
class GrapeReception(db.Model):
    __tablename__ = 'grape_reception'  # Nombre de la tabla en la base de datos

    # ID único generado con UUID4
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Nombre del proveedor o del lote recibido
    name = db.Column(db.String(100), nullable=False)  # nombre

    # Tipo de uva recibida (ej: Malbec, Cabernet)
    grape_type = db.Column(db.String(50), nullable=False)  # tipo

    # Cantidad de unidades o lotes recibidos
    quantity = db.Column(db.Integer, nullable=False)  # cantidad

    # Peso total de la recepción (en kilos, por ejemplo)
    weight = db.Column(db.Float, nullable=False)  # peso

    # Fecha en la que se recibió la uva (debe ser ingresada manualmente)
    reception_date = db.Column(db.Date, nullable=False)  # día de recepción
    
    #relacion con variety
    variety_id = db.Column(db.String(36), db.ForeignKey("variety.id"), nullable=False)
    variety = db.relationship("Variety", backref="receptions")

    # Representación como string
    def __repr__(self):
        return f"<GrapeReception {self.id} - {self.name} - {self.grape_type}>"
