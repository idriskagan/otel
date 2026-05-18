from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def role_required(*roles):
    """
    OTEL-11.1: Kullanıcının belirli rollere sahip olmasını zorunlu kılan dekoratör.
    Örnek: @role_required('admin') veya @role_required('admin', 'hotel_owner')
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Lütfen önce giriş yapın.', 'warning')
                return redirect(url_for('auth.login'))
                
            if current_user.role not in roles:
                flash('Bu sayfayı görüntülemek için yetkiniz yok.', 'danger')
                return redirect(url_for('main.index'))
                
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def hotel_owner_required(f):
    """OTEL-11.2: Sadece otel sahiplerinin (ve adminlerin) girebileceği rotalar için."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Lütfen önce giriş yapın.', 'warning')
            return redirect(url_for('auth.login'))
            
        if current_user.role not in ['hotel_owner', 'admin']:
            flash('Sadece otel sahipleri bu sayfaya erişebilir.', 'danger')
            return redirect(url_for('main.index'))
            
        return f(*args, **kwargs)
    return decorated_function