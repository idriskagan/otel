from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, FloatField, SubmitField, IntegerField, MultipleFileField
from wtforms.validators import DataRequired, Length, NumberRange, Optional
from flask_wtf.file import FileAllowed

class HotelForm(FlaskForm):
    """OTEL-16.1: Otel ekleme ve düzenleme formu."""
    name = StringField('Otel Adı', validators=[
        DataRequired(message="Otel adı zorunludur."),
        Length(min=3, max=200, message="Otel adı 3 ile 200 karakter arasında olmalıdır.")
    ])
    description = TextAreaField('Açıklama', validators=[
        Optional(),
        Length(max=2000, message="Açıklama çok uzun.")
    ])
    city = StringField('Şehir', validators=[
        DataRequired(message="Şehir bilgisi zorunludur."),
        Length(max=100)
    ])
    address = TextAreaField('Açık Adres', validators=[
        Optional(),
        Length(max=300)
    ])
    star_rating = SelectField('Yıldız Sayısı', choices=[
        ('1', '1 Yıldız'), ('2', '2 Yıldız'), ('3', '3 Yıldız'), 
        ('4', '4 Yıldız'), ('5', '5 Yıldız')
    ], default='3')
    phone = StringField('Telefon Numarası', validators=[Optional(), Length(max=20)])
    email = StringField('İletişim E-posta', validators=[Optional(), Length(max=120)])
    
    images = MultipleFileField('Otel Fotoğrafları (İsteğe bağlı)', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'Sadece resim dosyaları yüklenebilir!')
    ])
    
    submit = SubmitField('Kaydet')


class RoomTypeForm(FlaskForm):
    """OTEL-16.2: Oda tipi ekleme formu."""
    name = StringField('Oda Tipi Adı (Örn: Standart, Deluxe, Suit)', validators=[
        DataRequired(message="Oda tipi adı zorunludur."),
        Length(max=100)
    ])
    description = TextAreaField('Açıklama', validators=[Optional(), Length(max=500)])
    price_per_night = FloatField('Gecelik Fiyat (₺)', validators=[
        DataRequired(message="Gecelik fiyat zorunludur."),
        NumberRange(min=0, message="Fiyat 0'dan küçük olamaz.")
    ])
    capacity = IntegerField('Kişi Kapasitesi', validators=[
        DataRequired(message="Kapasite bilgisi zorunludur."),
        NumberRange(min=1, max=20, message="Kapasite en az 1 olmalıdır.")
    ])
    total_rooms = IntegerField('Toplam Oda Sayısı', validators=[
        DataRequired(message="Oda sayısı zorunludur."),
        NumberRange(min=1, message="Oda sayısı en az 1 olmalıdır.")
    ])
    submit = SubmitField('Oda Tipi Ekle')
