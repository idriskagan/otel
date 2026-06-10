from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange, ValidationError
from datetime import date

class ReservationForm(FlaskForm):
    """OTEL-16.3: Rezervasyon yapma formu."""
    check_in = DateField('Giriş Tarihi', validators=[DataRequired(message="Giriş tarihi zorunludur.")])
    check_out = DateField('Çıkış Tarihi', validators=[DataRequired(message="Çıkış tarihi zorunludur.")])
    guests = IntegerField('Kişi Sayısı', validators=[
        DataRequired(message="Kişi sayısı zorunludur."),
        NumberRange(min=1, message="En az 1 kişi olmalıdır.")
    ])
    submit = SubmitField('Rezervasyon Talebi Gönder')

    def validate_check_in(self, field):
        if field.data and field.data < date.today():
            raise ValidationError("Giriş tarihi bugünden önce olamaz.")

    def validate_check_out(self, field):
        if self.check_in.data and field.data and field.data <= self.check_in.data:
            raise ValidationError("Çıkış tarihi, giriş tarihinden sonra olmalıdır.")
