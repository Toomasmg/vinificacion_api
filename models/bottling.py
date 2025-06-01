
from models.db import db
class Bottling(db.Model):#embotellado
    __tablename__ = "bottling"
    id = db.Column(db.String(36), primary_key = True , default = lambda: str(uuid.uuid4())) #genera IDs unicos
    date_bottling = db.Column(db.Date, nullable = True) #fecha de produccion
    total_volume = db.Column(db.Float,nullable=True) #volumen total embotellado
    bottle_type = db.Column(db.Integer(),nullable=True) #tipo de botella(ej: 750ml, 375ml, etc.)
    bottle_quantity = db.Column(db.Integer(),nullable = True)#nro total de botellas producidas
    lot_number = db.Column(db.String(50),nullable=True,unique=True) # lote asociado
    observation = db.Column(db.Text,nullable=True)#observacion
    aging_id = db.Column(db.String(36), db.ForeignKey("aging.id"), nullable=True) #relacion con crianza
    def serialize(self):
        return {
            "id" : self.id,
            "date_bottling" : self.date_bottling,
            "total_volume" : self.total_volume,
            "bottle_type": self.bottle_type,
            "bottle_quantity": self.bottle_quantity,
            "lot_number": self.lot_number,
            "observation": self.observation,
            "aging_id" : self.aging_id,
        }