from wtforms import StringField, PasswordField, validators, ValidationError
from flask_wtf import FlaskForm
from .models import User


class RegistrationForm(FlaskForm):
    username = StringField('Nazwa', [validators.Length(min=4, max=25)])
    email = StringField('Adres email', [validators.Length(min=6, max=35)])
    password = PasswordField('Hasło', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Hasła muszą być takie same')
    ])
    confirm = PasswordField('Powtórz hasło')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Taki użytkownik istnieje')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Taki adres email istnieje')


class LoginForm(FlaskForm):
    email = StringField('Adres email', [validators.Length(min=6, max=35)])
    password = PasswordField('Hasło', [validators.DataRequired()])