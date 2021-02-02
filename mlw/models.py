from datetime import datetime
from config import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class MarinaLitterWatch(db.Model):
    __tablename__ = "mlw"
    mlw_id = db.Column(db.Integer, primary_key=True)
    appid = db.Column(db.String(32))
    hname = db.Column(db.String(32))
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class MarinaLitterWatchSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = MarinaLitterWatch
        include_fk = True
        include_relationships = True
        load_instance = True
