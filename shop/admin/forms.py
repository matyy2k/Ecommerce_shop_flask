from wtforms import StringField, PasswordField, validators, ValidationError, SubmitField, BooleanField
from flask_wtf import FlaskForm
from .models import Admin


class RegistrationForm(FlaskForm):
    username = StringField('Nazwa', [validators.Length(min=4, max=25)])
    email = StringField('Adres email', [validators.Length(min=6, max=35)])
    password = PasswordField('Hasło', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Hasła muszą być takie same')
    ])
    confirm = PasswordField('Powtórz hasło')
    submit = SubmitField('Zarejestruj')

    def validate_username(self, field):
        if Admin.query.filter_by(username=field.data).first():
            raise ValidationError('Taki użytkownik istnieje')

    def validate_email(self, field):
        if Admin.query.filter_by(email=field.data).first():
            raise ValidationError('Taki adres email istnieje')


class LoginForm(FlaskForm):
    email = StringField('Adres email', [validators.Length(min=6, max=35)])
    password = PasswordField('Hasło', [validators.DataRequired()])