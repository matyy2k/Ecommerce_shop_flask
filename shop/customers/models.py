from shop import app, db
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer, SignatureExpired


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
    email_confirmed = db.Column(db.Boolean(), nullable=False, default=False)

    def __repr__(self):
        return '<Klient %r>' % self.name

    def get_mail_confirm_token(self):
        s = URLSafeTimedSerializer(
            app.config["SECRET_KEY"], salt="email-comfirm"
        )
        return s.dumps(self.email, salt="email-confirm")

    @staticmethod
    def verify_mail_confirm_token(token):
        try:
            s = URLSafeTimedSerializer(
                app.config["SECRET_KEY"], salt="email-confirm"
            )
            email = s.loads(token, salt="email-confirm", max_age=3600)
            return email
        except SignatureExpired:
            return None


class CustomerOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    customer_id = db.Column(db.Integer, unique=False, nullable=False)
    discount = db.Column(db.Integer, default=0)


db.create_all()