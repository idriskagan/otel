from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import current_user, login_required
from app.services.reservation_service import ReservationService
from app.services.user_service import UserService
from app.services.favorite_service import FavoriteService
from app.forms.profile_forms import ProfileUpdateForm, ChangePasswordForm

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')
reservation_service = ReservationService()
user_service = UserService()
favorite_service = FavoriteService()

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

@dashboard_bp.route('/profile/edit', methods=['GET', 'POST'])
def profile_edit():
    """OTEL-28.4: Profil düzenleme sayfası."""
    form = ProfileUpdateForm(obj=current_user)
    
    if form.validate_on_submit():
        success, message = user_service.update_profile(
            user_id=current_user.id,
            data={
                'first_name': form.first_name.data,
                'last_name': form.last_name.data,
                'username': form.username.data,
                'email': form.email.data,
                'phone': form.phone.data,
                'bio': form.bio.data
            },
            avatar_file=request.files.get('avatar')
        )
        if success:
            flash(message, "success")
            return redirect(url_for('dashboard.index'))
        else:
            flash(message, "danger")
            
    return render_template('dashboard/profile_edit.html', form=form)

@dashboard_bp.route('/change-password', methods=['GET', 'POST'])
def change_password():
    """OTEL-28.6: Şifre değiştirme sayfası."""
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        success, message = user_service.change_password(
            user_id=current_user.id,
            current_password=form.current_password.data,
            new_password=form.new_password.data
        )
        if success:
            flash(message, "success")
            return redirect(url_for('dashboard.index'))
        else:
            flash(message, "danger")
            
    return render_template('dashboard/change_password.html', form=form)

@dashboard_bp.route('/favorites')
def favorites():
    """OTEL-29.4: Favori oteller sayfası."""
    favorite_hotels = favorite_service.get_user_favorites(current_user.id)
    return render_template('dashboard/favorites.html', hotels=favorite_hotels)

@dashboard_bp.route('/favorite/<int:hotel_id>', methods=['POST'])
def toggle_favorite(hotel_id):
    """OTEL-29.4: Favori ekle/çıkar (AJAX için uygun)."""
    success, message, is_favorited = favorite_service.toggle_favorite(current_user.id, hotel_id)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({
            'success': success,
            'message': message,
            'is_favorited': is_favorited
        })
        
    if success:
        flash(message, "success")
    else:
        flash(message, "danger")
    return redirect(request.referrer or url_for('hotel.list'))
