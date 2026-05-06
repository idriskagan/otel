from flask import Blueprint

hotel_owner_bp = Blueprint('hotel_owner', __name__)


@hotel_owner_bp.route('/dashboard')
def owner_dashboard():
    """Otel sahibi paneli — EPIC-4'te implementasyon."""
    return '<h1>Otel Sahibi Paneli</h1><p>EPIC-4 ile gelecek</p>'
