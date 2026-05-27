from flask import Blueprint, render_template
from app.repositories.hotel_repository import HotelRepository

main_bp = Blueprint('main', __name__)
hotel_repo = HotelRepository()


@main_bp.route('/')
def index():
    """Ana sayfa — onaylı otelleri listeler."""
    popular_hotels = hotel_repo.get_approved(page=1, per_page=6).items
    cities = hotel_repo.get_distinct_cities()
    return render_template('main/index.html', popular_hotels=popular_hotels, cities=cities)


@main_bp.route('/about')
def about():
    """Hakkında sayfası."""
    return render_template('main/about.html')
