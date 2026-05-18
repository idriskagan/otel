from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from app.services.reservation_service import ReservationService

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')
reservation_service = ReservationService()

@dashboard_bp.before_request
@login_required
def require_login():
    """Dashboard için giriş yapılmış olması zorunludur."""
    pass

@dashboard_bp.route('/')
def index():
    """OTEL-20.1: Profil sayfası."""
    return render_template('dashboard/user.html')

@dashboard_bp.route('/reservations')
def reservations():
    """OTEL-20.2: Kullanıcı rezervasyonları."""
    user_reservations = reservation_service.get_user_reservations(current_user.id)
    return render_template('dashboard/reservations.html', reservations=user_reservations)

@dashboard_bp.route('/reservation/<int:reservation_id>/cancel', methods=['POST'])
def cancel_reservation(reservation_id):
    """OTEL-20.3: Rezervasyon iptali."""
    success, message = reservation_service.cancel_reservation(reservation_id, current_user.id)
    if success:
        flash(message, "success")
    else:
        flash(message, "danger")
    return redirect(url_for('dashboard.reservations'))
