from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Ana sayfa."""
    return render_template('main/index.html')


@main_bp.route('/about')
def about():
    """Hakkında sayfası."""
    return render_template('main/about.html')
