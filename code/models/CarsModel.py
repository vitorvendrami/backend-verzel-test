from app import db


class Cars(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    picture_s3_url = db.Column(db.String(255), nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "brand": self.brand,
            "model": self.model,
            "picture_s3_url": self.picture_s3_url
        }
