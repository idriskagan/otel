from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from app.services.notification_service import NotificationService

notification_bp = Blueprint('notification', __name__)
notification_service = NotificationService()

@notification_bp.route('/')
@login_required
def list_notifications():
    """Kullanıcının tüm bildirimlerini listeler."""
    page = request.args.get('page', 1, type=int)
    notifications = notification_service.get_user_notifications(
        user_id=current_user.id,
        unread_only=False,
        page=page,
        per_page=15
    )
    return render_template('dashboard/notifications.html', notifications=notifications)

@notification_bp.route('/<int:id>/read', methods=['POST'])
@login_required
def mark_as_read(id):
    """Tek bir bildirimi okundu olarak işaretler."""
    notification = notification_service.mark_as_read(id)
    if not notification or notification.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'Yetkisiz veya geçersiz bildirim.'}), 403
    return jsonify({'success': True})

@notification_bp.route('/read-all', methods=['POST'])
@login_required
def mark_all_read():
    """Tüm bildirimleri okundu olarak işaretler."""
    notification_service.mark_all_as_read(current_user.id)
    return redirect(url_for('notification.list_notifications'))
