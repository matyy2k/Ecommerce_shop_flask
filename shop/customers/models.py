from shop import db, login_manager
from flask_login import UserMixin


class Customer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200), unique=False)
    country = db.Column(db.String(50), unique=False)
    city = db.Column(db.String(50), unique=False)
    contact = db.Column(db.String(50), unique=False)
    address = db.Column(db.String(50), unique=False)
    zipcode = db.Column(db.String(50), unique=False)

    def __repr__(self):
        return '<Klient %r>' % self.name


class CustomerOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    discount = db.Column(db.Integer, default=0)


db.create_all()