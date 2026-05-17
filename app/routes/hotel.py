from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from app.services.hotel_service import HotelService
from app.services.reservation_service import ReservationService
from app.services.review_service import ReviewService
from app.forms.reservation_forms import ReservationForm

hotel_bp = Blueprint('hotel', __name__, url_prefix='/hotels')

hotel_service = HotelService()
reservation_service = ReservationService()
review_service = ReviewService()

@hotel_bp.route('/')
def list_hotels():
    """OTEL-17.1: Onaylanmış otelleri listeler."""
    page = request.args.get('page', 1, type=int)
    # Servis filter ile de listelenebilir.
    hotels = hotel_service.hotel_repo.get_approved(page=page, per_page=12)
    return render_template('hotel/list.html', hotels=hotels)

@hotel_bp.route('/search')
def search():
    """OTEL-17.3: Otelleri filtreler."""
    city = request.args.get('city')
    min_stars = request.args.get('stars', type=int)
    
    hotels = hotel_service.search_hotels(city=city, min_stars=min_stars, is_approved=True)
    return render_template('hotel/search.html', hotels=hotels, city=city, stars=min_stars)

@hotel_bp.route('/<int:hotel_id>')
def hotel_detail(hotel_id):
    """OTEL-17.2: Otel detay sayfası."""
    hotel = hotel_service.hotel_repo.get_by_id(hotel_id)
    if not hotel or not hotel.is_approved:
        flash("Otel bulunamadı veya henüz onaylanmadı.", "danger")
        return redirect(url_for('hotel.list_hotels'))
        
    form = ReservationForm()
    
    # Yorumları getir
    page = request.args.get('page', 1, type=int)
    reviews_data = review_service.get_hotel_reviews(hotel_id, page=page)
    
    return render_template('hotel/detail.html', hotel=hotel, form=form, reviews_data=reviews_data)

@hotel_bp.route('/<int:hotel_id>/reserve', methods=['POST'])
@login_required
def reserve(hotel_id):
    """OTEL-17.4: Rezervasyon talebi."""
    hotel = hotel_service.hotel_repo.get_by_id(hotel_id)
    if not hotel or not hotel.is_approved:
        flash("Geçersiz işlem.", "danger")
        return redirect(url_for('hotel.list_hotels'))
        
    form = ReservationForm()
    if form.validate_on_submit():
        room_type_id = request.form.get('room_type_id', type=int)
        if not room_type_id:
            flash("Lütfen bir oda tipi seçin.", "warning")
            return redirect(url_for('hotel.hotel_detail', hotel_id=hotel_id))
            
        success, message, res = reservation_service.create_reservation(
            user_id=current_user.id,
            room_type_id=room_type_id,
            hotel_id=hotel_id,
            check_in=form.check_in.data,
            check_out=form.check_out.data,
            guests=form.guests.data
        )
        if success:
            flash(message, "success")
            return redirect(url_for('dashboard.reservations'))
        else:
            flash(message, "danger")
            
    return redirect(url_for('hotel.hotel_detail', hotel_id=hotel_id))

@hotel_bp.route('/<int:hotel_id>/review', methods=['POST'])
@login_required
def review(hotel_id):
    """OTEL-17.5: Otele yorum ekle."""
    rating = request.form.get('rating', type=int)
    comment = request.form.get('comment')
    
    if not rating or not comment:
        flash("Puan ve yorum zorunludur.", "warning")
        return redirect(url_for('hotel.hotel_detail', hotel_id=hotel_id))
        
    success, message, rev = review_service.add_review(
        user_id=current_user.id,
        hotel_id=hotel_id,
        rating=rating,
        comment=comment
    )
    
    if success:
        flash(message, "success")
    else:
        flash(message, "danger")
        
    return redirect(url_for('hotel.hotel_detail', hotel_id=hotel_id))
