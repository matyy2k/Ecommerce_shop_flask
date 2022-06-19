from wtforms import StringField, PasswordField, validators, ValidationError, SubmitField
from flask_wtf import FlaskForm
from .models import Admin


class RegistrationForm(FlaskForm):
    username = StringField('Nazwa', [validators.Length(min=3, max=30)])
    email = StringField('Adres email', [validators.Regexp('(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9]+\.[a-zA-Z0-9.]*\.*['
                                                          'com|org|edu]{3}$)', message="Mail nie spełnia wymagań")])
    password = PasswordField('Hasło', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Hasła muszą być takie same')
    ])
    confirm = PasswordField('Powtórz hasło')
    admin = StringField('Admin', default=True)
    moderator = StringField('Moderator', default=False)
    submit = SubmitField('Zarejestruj')

    def validate_username(self, field):
        if Admin.query.filter_by(username=field.data).first():
            raise ValidationError('Taki użytkownik istnieje')

    def validate_email(self, field):
        if Admin.query.filter_by(email=field.data).first():
            raise ValidationError('Taki adres email istnieje')


class LoginForm(FlaskForm):
    email = StringField('Adres email', [validators.Length(min=5, max=30)])
    password = PasswordField('Hasło', [validators.DataRequired()])