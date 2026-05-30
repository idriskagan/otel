from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify 
from flask_login import current_user, login_required
from app.services.hotel_service import HotelService
from app.services.reservation_service import ReservationService
from app.services.review_service import ReviewService
from app.forms.reservation_forms import ReservationForm
from app.services.chatbot_service import ChatbotService

hotel_bp = Blueprint('hotel', __name__, url_prefix='/hotels')

hotel_service = HotelService()
reservation_service = ReservationService()
review_service = ReviewService()
chatbot_service = ChatbotService()

@hotel_bp.route('/')
def list_hotels():
    """OTEL-17.1: Onaylanmış otelleri listeler. (Tüm istekleri search'e yönlendirir)"""
    return redirect(url_for('hotel.search'))

@hotel_bp.route('/search')
def search():
    """OTEL-17.3 & OTEL-30: Otelleri gelişmiş filtreler ile arar."""
    from app.models.amenity import Amenity
    from app.extensions import db
    
    city = request.args.get('city')
    min_stars = request.args.get('stars', type=int)
    price_min = request.args.get('price_min', type=float)
    price_max = request.args.get('price_max', type=float)
    check_in = request.args.get('check_in')
    check_out = request.args.get('check_out')
    sort_by = request.args.get('sort_by', 'newest')
    amenity_ids = request.args.getlist('amenities', type=int)
    page = request.args.get('page', 1, type=int)
    
    pagination = hotel_service.search_hotels(
        city=city, min_stars=min_stars,
        price_min=price_min, price_max=price_max,
        amenity_ids=amenity_ids,
        check_in=check_in, check_out=check_out,
        sort_by=sort_by,
        page=page, per_page=12
    )
    
    # Tüm amenityleri kategorilerine göre grupla
    amenities = db.session.execute(db.select(Amenity).order_by(Amenity.category, Amenity.name)).scalars().all()
    amenity_groups = {}
    for a in amenities:
        if a.category not in amenity_groups:
            amenity_groups[a.category] = []
        amenity_groups[a.category].append(a)
    
    return render_template('hotel/list.html', 
                           hotels=pagination, 
                           city=city, stars=min_stars,
                           price_min=price_min, price_max=price_max,
                           check_in=check_in, check_out=check_out,
                           sort_by=sort_by,
                           selected_amenities=amenity_ids,
                           amenity_groups=amenity_groups)

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
    sort_by = request.args.get('sort_by', 'newest')
    reviews_data = review_service.get_hotel_reviews(hotel_id, page=page, sort_by=sort_by)
    
    return render_template('hotel/detail.html', hotel=hotel, form=form, reviews_data=reviews_data, sort_by=sort_by)

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

@hotel_bp.route('/review/<int:review_id>/edit', methods=['POST'])
@login_required
def edit_review(review_id):
    """OTEL-31.1: Yorum düzenleme."""
    rating = request.form.get('rating', type=int)
    comment = request.form.get('comment')
    success, message = review_service.edit_review(review_id, current_user.id, rating, comment)
    if success:
        flash(message, "success")
    else:
        flash(message, "danger")
    return redirect(request.referrer or url_for('hotel.list_hotels'))

@hotel_bp.route('/review/<int:review_id>/delete', methods=['POST'])
@login_required
def delete_review(review_id):
    """OTEL-31.1: Yorum silme."""
    success, message = review_service.delete_review(review_id, current_user.id)
    if success:
        flash(message, "success")
    else:
        flash(message, "danger")
    return redirect(request.referrer or url_for('hotel.list_hotels'))

@hotel_bp.route('/review/<int:review_id>/reply', methods=['POST'])
@login_required
def reply_review(review_id):
    """OTEL-31.2: Yorum yanıtlama (otel sahibi için)."""
    comment = request.form.get('comment')
    success, message = review_service.add_reply(review_id, current_user.id, comment)
    if success:
        flash(message, "success")
    else:
        flash(message, "danger")
    return redirect(request.referrer or url_for('hotel.list_hotels'))

@hotel_bp.route('/review/<int:review_id>/helpful', methods=['POST'])
@login_required
def helpful_review(review_id):
    """OTEL-31.5: Yorum faydalı."""
    from flask import jsonify
    success, message = review_service.vote_helpful(review_id)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': success, 'message': message})
    if success:
        flash(message, "success")
    else:
        flash(message, "danger")
    return redirect(request.referrer or url_for('hotel.list_hotels'))

@hotel_bp.route('/<int:hotel_id>/chat', methods=['POST'])
def hotel_chatbot(hotel_id):
    """OTEL-CHATBOT: Gemini destekli otel bilgi asistanı (Service Entegreli)."""
    data = request.get_json()
    
    if not data or not data.get('message'):
        return jsonify({'success': False, 'message': 'Lütfen bir mesaj gönderin.'}), 400
        
    user_message = data['message']
    
    # Tüm ağır işi Service katmanına devrediyoruz
    success, response_message = chatbot_service.ask_hotel_assistant(hotel_id, user_message)
    
    if success:
        return jsonify({'success': True, 'reply': response_message})
    else:
        # Eğer success False dönerse, response_message içinde hata detayı vardır
        status_code = 404 if "bulunamadı" in response_message else 500
        return jsonify({'success': False, 'message': response_message}), status_code
