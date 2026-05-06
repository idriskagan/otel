from flask import Blueprint

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
def user_dashboard():
    """Kullanıcı paneli — EPIC-4'te implementasyon."""
    return '<h1>Kullanıcı Paneli</h1><p>EPIC-4 ile gelecek</p>'
