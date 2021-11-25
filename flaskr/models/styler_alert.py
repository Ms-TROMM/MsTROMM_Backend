from ..main import db


class Clothes(db.Model):
    __tablename__ = 'clothes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
