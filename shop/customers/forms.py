from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators, ValidationError
from .models import Customer


class CustomerRegisterForm(FlaskForm):
    username = StringField('Nazwa', [validators.Length(min=3, max=30)])
    email = StringField('Adres email', [validators.Regexp('(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9]+\.[a-zA-Z0-9.]*\.*['
                                                          'com|org|edu]{3}$)', message="Mail nie spełnia wymagań")])
    password = PasswordField('Hasło', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Hasła muszą być takie same')
    ])
    confirm = PasswordField('Powtórz hasło')
    country = StringField('Państwo', [validators.DataRequired()])
    city = StringField('Miasto', [validators.DataRequired()])
    contact = StringField('Numer telefonu', [validators.DataRequired()])
    address = StringField('Adres zamieszkania', [validators.DataRequired()])
    zipcode = StringField('Kod pocztowy', [validators.DataRequired()])
    submit = SubmitField('Zarejestruj')

    def validate_username(self, username):
        if Customer.query.filter_by(username=username.data).first():
            raise ValidationError("Taki użytkownik istnieje")

    def validate_email(self, email):
        if Customer.query.filter_by(email=email.data).first():
            raise ValidationError("Taki adres email istnieje")


class CustomerLoginForm(FlaskForm):
    email = StringField('Adres email', [validators.Length(min=5, max=30)])
    password = PasswordField('Hasło', [validators.DataRequired()])