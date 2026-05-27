from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from app.utils.decorators import hotel_owner_required
from app.services.hotel_service import HotelService
from app.forms.hotel_forms import HotelForm, RoomTypeForm
from app.models.room import RoomType

hotel_owner_bp = Blueprint('hotel_owner', __name__, url_prefix='/owner')
hotel_service = HotelService()

@hotel_owner_bp.before_request
@login_required
@hotel_owner_required
def require_owner():
    """Tüm owner rotaları için owner yetkisi gerektirir."""
    pass

@hotel_owner_bp.route('/dashboard')
def dashboard():
    """OTEL-18.1: Otel sahibi paneli."""
    hotels = hotel_service.hotel_repo.get_by_owner(current_user.id)
    return render_template('dashboard/owner.html', hotels=hotels)

@hotel_owner_bp.route('/hotel/new', methods=['GET', 'POST'])
def new_hotel():
    """OTEL-18.2: Yeni otel ekleme."""
    form = HotelForm()
    if form.validate_on_submit():
        success, message, hotel = hotel_service.create_hotel(
            owner_id=current_user.id,
            data={
                'name': form.name.data,
                'description': form.description.data,
                'city': form.city.data,
                'address': form.address.data,
                'star_rating': form.star_rating.data,
                'phone': form.phone.data,
                'email': form.email.data
            }
        )
        if success:
            # Resim varsa yükle
            if form.images.data and form.images.data[0].filename:
                hotel_service.upload_images(hotel.id, current_user.id, request.files.getlist('images'))
            
            flash(message, "success")
            return redirect(url_for('hotel_owner.dashboard'))
        else:
            flash(message, "danger")
            
    return render_template('dashboard/owner_hotel_form.html', form=form, title="Yeni Otel Ekle")

@hotel_owner_bp.route('/hotel/<int:hotel_id>/edit', methods=['GET', 'POST'])
def edit_hotel(hotel_id):
    """OTEL-18.3: Otel düzenleme."""
    hotel = hotel_service.hotel_repo.get_by_id(hotel_id)
    if not hotel or hotel.owner_id != current_user.id:
        flash("Yetkisiz işlem.", "danger")
        return redirect(url_for('hotel_owner.dashboard'))
        
    form = HotelForm(obj=hotel)
    # star_rating bir int'ten string selectbox'a döner
    if request.method == 'GET':
        form.star_rating.data = str(hotel.star_rating)
        
    if form.validate_on_submit():
        success, message, updated_hotel = hotel_service.update_hotel(
            hotel_id=hotel_id,
            owner_id=current_user.id,
            data={
                'name': form.name.data,
                'description': form.description.data,
                'city': form.city.data,
                'address': form.address.data,
                'star_rating': form.star_rating.data,
                'phone': form.phone.data,
                'email': form.email.data
            }
        )
        if success:
            if form.images.data and form.images.data[0].filename:
                hotel_service.upload_images(hotel_id, current_user.id, request.files.getlist('images'))
            flash(message, "success")
            return redirect(url_for('hotel_owner.dashboard'))
        else:
            flash(message, "danger")
            
    return render_template('dashboard/owner_hotel_form.html', form=form, title="Oteli Düzenle")

@hotel_owner_bp.route('/hotel/<int:hotel_id>/delete', methods=['POST'])
def delete_hotel(hotel_id):
    """OTEL-18.4: Otel silme."""
    hotel = hotel_service.hotel_repo.get_by_id(hotel_id)
    if not hotel or hotel.owner_id != current_user.id:
        flash("Yetkisiz işlem.", "danger")
        return redirect(url_for('hotel_owner.dashboard'))
        
    try:
        hotel_service.hotel_repo.delete(hotel)
        hotel_service.hotel_repo.commit()
        flash("Otel başarıyla silindi.", "success")
    except Exception as e:
        hotel_service.hotel_repo.rollback()
        flash(f"Otel silinirken hata oluştu: {str(e)}", "danger")
        
    return redirect(url_for('hotel_owner.dashboard'))

@hotel_owner_bp.route('/hotel/<int:hotel_id>/rooms', methods=['GET', 'POST'])
def hotel_rooms(hotel_id):
    """OTEL-18.5: Oda tipi ekleme/yönetme."""
    hotel = hotel_service.hotel_repo.get_by_id(hotel_id)
    if not hotel or hotel.owner_id != current_user.id:
        flash("Yetkisiz işlem.", "danger")
        return redirect(url_for('hotel_owner.dashboard'))
        
    form = RoomTypeForm()
    if form.validate_on_submit():
        try:
            from app.extensions import db
            room = RoomType(
                hotel_id=hotel_id,
                name=form.name.data,
                description=form.description.data,
                price_per_night=form.price_per_night.data,
                capacity=form.capacity.data,
                total_rooms=form.total_rooms.data
            )
            db.session.add(room)
            db.session.commit()
            flash("Oda tipi eklendi.", "success")
            return redirect(url_for('hotel_owner.hotel_rooms', hotel_id=hotel_id))
        except Exception as e:
            flash(f"Hata oluştu: {str(e)}", "danger")
            
    return render_template('dashboard/owner_rooms.html', hotel=hotel, form=form)
