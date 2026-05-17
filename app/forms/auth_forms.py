from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class LoginForm(FlaskForm):
    """OTEL-9.1: Kullanıcı giriş formu."""
    email = StringField('E-posta', validators=[
        DataRequired(message='E-posta alanı zorunludur.'),
        Email(message='Geçerli bir e-posta adresi giriniz.')
    ])
    password = PasswordField('Şifre', validators=[
        DataRequired(message='Şifre alanı zorunludur.')
    ])
    remember = BooleanField('Beni Hatırla')
    submit = SubmitField('Giriş Yap')


class RegisterForm(FlaskForm):
    """OTEL-9.2: Yeni kullanıcı kayıt formu."""
    username = StringField('Kullanıcı Adı', validators=[
        DataRequired(message='Kullanıcı adı zorunludur.'),
        Length(min=3, max=80, message='Kullanıcı adı 3 ile 80 karakter arasında olmalıdır.')
    ])
    email = StringField('E-posta', validators=[
        DataRequired(message='E-posta alanı zorunludur.'),
        Email(message='Geçerli bir e-posta adresi giriniz.')
    ])
    password = PasswordField('Şifre', validators=[
        DataRequired(message='Şifre alanı zorunludur.'),
        Length(min=6, message='Şifre en az 6 karakter olmalıdır.')
    ])
    confirm_password = PasswordField('Şifre Tekrar', validators=[
        DataRequired(message='Lütfen şifrenizi tekrar girin.'),
        EqualTo('password', message='Şifreler birbiriyle eşleşmiyor.')
    ])
    role = SelectField('Hesap Türü', choices=[
        ('user', 'Misafir (Otel arıyorum)'),
        ('hotel_owner', 'Otel Sahibi (Otelimi eklemek istiyorum)')
    ])
    submit = SubmitField('Kayıt Ol')
