from extensions import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    price = db.Column(db.Numeric(8,2), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    availability = db.Column(db.Boolean, nullable=False, default=True)
    category = db.Column(db.String(120), nullable=False)
    image = db.Column(db.String(120), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "price": float(self.price),
            "rating": self.rating,
            "availability": self.availability,
            "category": self.category,
            "image": self.image
        }
