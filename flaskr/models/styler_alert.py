from .. main import db
from marshmallow import Schema, fields

class StylerAlert(db.Model):
    __tablename__ = 'styler_alert'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

    def __init__(self, user_id, title, description):
        self.user_id = user_id
        self.title = title
        self.description = description
    
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

class alertSchema(Schema):
    id = fields.Integer()
    user_id = fields.Integer()
    title = fields.String()
    description = fields.String()
    created_at = fields.DateTime()