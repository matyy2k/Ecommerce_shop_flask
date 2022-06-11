from wtforms import StringField, PasswordField, validators, ValidationError
from flask_wtf import FlaskForm


class LoginForm(FlaskForm):
    email = StringField('Adres email', [validators.Length(min=6, max=35)])
    password = PasswordField('Hasło', [validators.DataRequired()])