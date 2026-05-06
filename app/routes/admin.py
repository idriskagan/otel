from flask import Blueprint

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/dashboard')
def admin_dashboard():
    """Admin paneli — EPIC-4'te implementasyon."""
    return '<h1>Admin Paneli</h1><p>EPIC-4 ile gelecek</p>'
