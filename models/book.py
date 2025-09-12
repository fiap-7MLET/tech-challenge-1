from extensions import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    price = db.Column(db.Numeric(8,2), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    availability = db.Column(db.Boolean, nullable=False, default=True)
    category = db.Column(db.String(120), nullable=False)
    image = db.Column(db.String(120), nullable=True)
