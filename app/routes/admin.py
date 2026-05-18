from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from app.utils.decorators import role_required
from app.services.hotel_service import HotelService
from app.repositories.user_repository import UserRepository
from app.repositories.reservation_repository import ReservationRepository

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

hotel_service = HotelService()
user_repo = UserRepository()
res_repo = ReservationRepository()

@admin_bp.before_request
@login_required
@role_required('admin')
def require_admin():
    """Tüm admin rotaları için admin yetkisi gerektirir."""
    pass

@admin_bp.route('/dashboard')
def dashboard():
    """OTEL-19.1: Admin paneli ve istatistikler."""
    stats = {
        'total_users': user_repo.count_all(),
        'total_hotels': hotel_service.hotel_repo.count_all(),
        'total_reservations': res_repo.count_all()
    }
    return render_template('admin/dashboard.html', stats=stats)

@admin_bp.route('/hotels')
def hotels():
    """OTEL-19.2: Tüm otelleri listeler."""
    page = request.args.get('page', 1, type=int)
    # Admin tüm otelleri (onaylı/onaysız) görebilmeli.
    pagination = hotel_service.hotel_repo.paginate(page=page, per_page=20)
    return render_template('admin/hotels.html', pagination=pagination)

@admin_bp.route('/hotels/<int:hotel_id>/approve', methods=['POST'])
def approve_hotel(hotel_id):
    """OTEL-19.2: Oteli onaylar."""
    success, message = hotel_service.approve_hotel(hotel_id)
    if success:
        flash(message, "success")
    else:
        flash(message, "danger")
    return redirect(url_for('admin.hotels'))

@admin_bp.route('/users')
def users():
    """OTEL-19.3: Tüm kullanıcıları listeler."""
    page = request.args.get('page', 1, type=int)
    pagination = user_repo.paginate(page=page, per_page=20)
    return render_template('admin/users.html', pagination=pagination)

@admin_bp.route('/users/<int:user_id>/toggle', methods=['POST'])
def toggle_user(user_id):
    """OTEL-19.3: Kullanıcıyı aktif/pasif yapar."""
    user = user_repo.get_by_id(user_id)
    if not user:
        flash("Kullanıcı bulunamadı.", "danger")
    elif user.id == current_user.id:
        flash("Kendinizi pasife alamazsınız.", "warning")
    else:
        user.is_active = not user.is_active
        user_repo.update(user)
        user_repo.commit()
        status = "aktif" if user.is_active else "pasif"
        flash(f"Kullanıcı {status} duruma getirildi.", "success")
        
    return redirect(url_for('admin.users'))
