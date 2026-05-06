from flask import Blueprint

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login')
def login():
    """Giriş sayfası — EPIC-3'te implementasyon."""
    return '<h1>Giriş Sayfası</h1><p>EPIC-3 ile gelecek</p>'


@auth_bp.route('/register')
def register():
    """Kayıt sayfası — EPIC-3'te implementasyon."""
    return '<h1>Kayıt Sayfası</h1><p>EPIC-3 ile gelecek</p>'


@auth_bp.route('/logout')
def logout():
    """Çıkış — EPIC-3'te implementasyon."""
    return '<h1>Çıkış</h1>'
