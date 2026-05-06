from flask import Blueprint

hotel_bp = Blueprint('hotel', __name__)


@hotel_bp.route('/')
def list_hotels():
    """Otel listesi — EPIC-4'te implementasyon."""
    return '<h1>Oteller</h1><p>EPIC-4 ile gelecek</p>'


@hotel_bp.route('/<int:hotel_id>')
def hotel_detail(hotel_id):
    """Otel detay — EPIC-4'te implementasyon."""
    return f'<h1>Otel #{hotel_id}</h1><p>EPIC-4 ile gelecek</p>'
