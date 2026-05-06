import os
from flask import Flask
from dotenv import load_dotenv

from app.config import config
from app.extensions import db, migrate, login_manager, csrf


def create_app(config_name=None):
    """Application Factory Pattern — Flask uygulamasını oluşturur ve yapılandırır."""

    # .env dosyasını yükle
    load_dotenv()

    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Upload klasörünü oluştur
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Extension'ları başlat
    _register_extensions(app)

    # Blueprint'leri kaydet
    _register_blueprints(app)

    # User loader callback
    _register_user_loader()

    return app


def _register_extensions(app):
    """Flask extension'larını uygulamaya bağlar."""
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)


def _register_blueprints(app):
    """Tüm Blueprint'leri uygulamaya kaydeder."""
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.hotel import hotel_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.hotel_owner import hotel_owner_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(hotel_bp, url_prefix='/hotels')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(hotel_owner_bp, url_prefix='/owner')
    app.register_blueprint(admin_bp, url_prefix='/admin')


def _register_user_loader():
    """Flask-Login user_loader callback'ini kaydeder."""
    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))
