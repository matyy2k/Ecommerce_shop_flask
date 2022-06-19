from wtforms import Form, IntegerField, FloatField, StringField, TextAreaField, validators
from flask_wtf.file import FileField, FileRequired, FileAllowed


class Products(Form):
    name = StringField('Nazwa', [validators.DataRequired()])
    price = FloatField('Cena', [validators.DataRequired()])
    discount = IntegerField('Zniżka', [validators.DataRequired()])
    stock = IntegerField('Ilość', [validators.DataRequired()])
    description = TextAreaField('Opis', [validators.DataRequired()])
    image = FileField('Zdjęcie', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'])])