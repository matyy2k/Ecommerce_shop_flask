from shop import db, login_manager
from flask_login import UserMixin


class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(180), unique=False, nullable=False)
    admin = db.Column(db.String(), default=True, server_default="true")
    moderator = db.Column(db.String(), default=False, server_default="false")

    def __repr__(self):
        return f'Użytkownik: {self.username}'


db.create_all()