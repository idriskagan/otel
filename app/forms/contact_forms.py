from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class ContactForm(FlaskForm):
    """OTEL-34.1: İletişim formu."""
    name = StringField('Adınız Soyadınız', validators=[
        DataRequired(message="Ad soyad zorunludur."),
        Length(min=2, max=100, message="Ad soyad 2 ile 100 karakter arasında olmalıdır.")
    ])
    email = StringField('E-posta Adresiniz', validators=[
        DataRequired(message="E-posta zorunludur."),
        Email(message="Lütfen geçerli bir e-posta adresi girin.")
    ])
    subject = StringField('Konu', validators=[
        DataRequired(message="Konu zorunludur."),
        Length(min=3, max=150, message="Konu 3 ile 150 karakter arasında olmalıdır.")
    ])
    message = TextAreaField('Mesajınız', validators=[
        DataRequired(message="Mesaj zorunludur."),
        Length(min=10, message="Mesajınız en az 10 karakter olmalıdır.")
    ])
    submit = SubmitField('Mesaj Gönder')
