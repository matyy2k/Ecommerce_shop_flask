from wtforms import Form, StringField, TextAreaField, PasswordField, SubmitField, validators, ValidationError
from flask_wtf.file import FileRequired, FileAllowed, FileField
from flask_wtf import FlaskForm
from .model import Register


class CustomerRegisterForm(FlaskForm):
    name = StringField('Imię')
    username = StringField('Nazwa użytkownika', [validators.DataRequired()])
    email = StringField('Adres email', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Hasło', [validators.DataRequired(), validators.EqualTo('confirm', message=' Hasła '
                                                                                                        'muszą '
                                                                                                        'pasować ')])
    confirm = PasswordField('Powtórz hasło', [validators.DataRequired()])
    country = StringField('Państwo', [validators.DataRequired()])
    city = StringField('Miasto', [validators.DataRequired()])
    contact = StringField('Numer telefonu', [validators.DataRequired()])
    address = StringField('Adres zamieszkania', [validators.DataRequired()])
    zipcode = StringField('Kod pocztowy', [validators.DataRequired()])

    submit = SubmitField('Zarejestruj')

    def validate_username(self, username):
        if Register.query.filter_by(username=username.data).first():
            raise ValidationError("Taki użytkownik istnieje")

    def validate_email(self, email):
        if Register.query.filter_by(email=email.data).first():
            raise ValidationError("Taki adres email istnieje")


class customer_loginFrom(FlaskForm):
    email = StringField('Email', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Hasło', [validators.DataRequired()])