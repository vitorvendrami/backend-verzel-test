from app import db


class Cars(db.Model):
    """Cars Model"""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(
        db.String(50), unique=True, nullable=False, default="SUZUKI VITARA 4YOU"
    )
    description = db.Column(db.String(100), default="This is a brand new car")
    photo = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=True, default=2022)
    km = db.Column(db.Integer, nullable=True, default=0)
    city = db.Column(db.String(100), default="Sao Paulo")
    price = db.Column(db.Integer, nullable=True, default=10000)
    category_id = db.Column(db.Integer, nullable=True, default=1)

    def get_category_json(self, category_id):
        """Maps a category given it's id"""
        CATEGORY_MAP = {
            1: "SUV",
            2: "HATCH",
            3: "CROSSOVER",
            4: "CONVERTIBLE",
            5: "SEDAN",
        }

        category = {"id": category_id, "label": CATEGORY_MAP[category_id]}

        return category

    def to_json(self):
        """JSON representation of the model"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "photo": self.photo,
            "year": self.year,
            "km": self.km,
            "city": self.city,
            "price": self.price,
            "category": self.get_category_json(self.category_id),
        }
