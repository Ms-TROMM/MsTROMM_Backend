import enum
from ..main import db
from marshmallow import Schema, fields


class ClothesType(enum.Enum):
    top = 0
    down = 1
    outwear = 2
    onepiece = 3


class Clothes(db.Model):
    __tablename__ = 'clothes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    clothes_type = db.Column(db.Enum(ClothesType))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(30))
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    stylered_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    need_styler = db.Column(db.Integer, default=0) # if the clothes needs to be in styler,
    # this value is set to 1, otherwise 0
    is_inside_styler = db.Column(db.Integer, default=0)
    color = db.Column(db.Integer) # Must convert hexadecimal color value to integer before inserting into database
    texture = db.Column(db.String(50))
    
    def __init__(self, clothes_type, user_id, name, created_at, stylered_at, need_styler, is_inside_styler, color, texture):
        self.clothes_type = clothes_type
        self.user_id = user_id
        self.name = name
        self.created_at = created_at
        self.stylered_at = stylered_at
        self.need_styler = need_styler
        self.is_inside_styler = is_inside_styler
        self.color = color
        self.texture = texture
        
class clotheSchema(Schema):
    id = fields.Integer()
    clothes_type = fields.String()
    user_id = fields.Integer()
    name = fields.String()
    created_at = fields.DateTime()
    stylered_at = fields.DateTime()
    need_styler = fields.Integer()
    is_inside_styler = fields.Integer()
    color = fields.Integer()
    texture = fields.String()       
        

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
