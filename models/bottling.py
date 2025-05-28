
from models.db import db
class Bottling(db.Model):#embotellado
    __tablename__ = "bottling"
    id = db.Column(db.String(36), primary_key = True , default = lambda: str(uuid.uuid4())) #genera IDs unicos
    date_bottling = db.Column(db.Date, nullable = True) #fecha de produccion
    bottling_code = db.Column(db.String(100), unique=True, nullable=True) #codigo unico del botella
    aging_id = db.Column(db.String(36), db.ForeignKey("aging.id"), nullable=True) #relacion con crianza

    def serialize(self):
        return {
            "id" : self.id,
            "date_bottling" : self.date_bottling,
            "bottling_code" : self.bottling_code,
            "aging_id" : self.aging_id,
        }