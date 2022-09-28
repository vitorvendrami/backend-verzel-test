from app import db
from scripts.DatabaseAdmin import DatabaseAdmin


class Users(db.Model):
    """Users Model"""

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(50))
    admin = db.Column(db.Boolean)

    def to_json(self):
        return {"id": self.id, "email": self.email, "admin": self.admin}
