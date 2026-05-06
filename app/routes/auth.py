from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user

from app.forms.auth_forms import LoginForm, RegisterForm
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)

# Repository ve Service instance'ları
user_repo = UserRepository()
auth_service = AuthService(user_repo)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """OTEL-10.2: Kullanıcı giriş sayfası."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        success, message = auth_service.authenticate_and_login(
            email=form.email.data,
            password=form.password.data,
            remember=form.remember.data
        )
        
        if success:
            flash(message, 'success')
            # Kullanıcı daha önceden login sayfasına zorla yönlendirildiyse, oraya geri dön
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.index'))
        else:
            flash(message, 'danger')

    return render_template('auth/login.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """OTEL-10.3: Yeni kullanıcı kayıt sayfası."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegisterForm()
    if form.validate_on_submit():
        success, message = auth_service.register_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            role=form.role.data
        )
        
        if success:
            flash(message, 'success')
            return redirect(url_for('auth.login'))
        else:
            flash(message, 'danger')

    return render_template('auth/register.html', form=form)


@auth_bp.route('/logout')
def logout():
    """OTEL-10.4: Oturum kapatma."""
    auth_service.logout()
    flash('Başarıyla çıkış yaptınız.', 'info')
    return redirect(url_for('main.index'))
