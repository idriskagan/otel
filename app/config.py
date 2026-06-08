import os

# 1. ORTAM DEĞİŞKENİNİ AL VE DÜZELT
# Render veya Neon'dan gelen DATABASE_URL'i okuyoruz.
database_url = os.environ.get('DATABASE_URL')

# Eğer bir URL varsa ve 'postgres://' ile başlıyorsa, bunu SQLAlchemy için düzeltiyoruz.
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)


class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-secret-key-change-in-production')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'uploads')
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    # 2. DÜZELTİLMİŞ URL'İ KULLAN
    # Eğer ortamda DATABASE_URL varsa onu (Neon) kullan, yoksa lokaldeki (otel.db) ile devam et.
    SQLALCHEMY_DATABASE_URI = database_url or 'sqlite:///otel.db'


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    # Canlı ortamda sadece düzeltilmiş PostgreSQL URL'ini kullanır.
    SQLALCHEMY_DATABASE_URI = database_url


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    # Testler sırasında hafızada çalışan hızlı ve geçici bir SQLite kullanmaya devam eder.
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
