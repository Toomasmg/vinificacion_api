from models.db import db
import uuid

class Aging(db.Model):
    __tablename__ = "aging"
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    def serialize(self):
        return {
            "id":self.id,
        }