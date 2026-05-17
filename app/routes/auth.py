from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, logout_user, current_user
from app.forms.auth_forms import LoginForm, RegisterForm
from app.services.auth_service import AuthService
from urllib.parse import urlsplit

auth_bp = Blueprint('auth', __name__)
auth_service = AuthService()

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Kullanıcı kayıt sayfası."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    form = RegisterForm()
    if form.validate_on_submit():
        success, message, user = auth_service.register_user({
            'username': form.username.data,
            'email': form.email.data,
            'password': form.password.data,
            'role': form.role.data
        })
        
        if success:
            flash(message, 'success')
            return redirect(url_for('auth.login'))
        else:
            flash(message, 'danger')
            
    return render_template('auth/register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Kullanıcı giriş sayfası."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    form = LoginForm()
    if form.validate_on_submit():
        success, message, user = auth_service.authenticate_user(
            email=form.email.data,
            password=form.password.data,
            remember=form.remember.data
        )
        
        if success:
            flash(message, 'success')
            next_page = request.args.get('next')
            if not next_page or urlsplit(next_page).netloc != '':
                next_page = url_for('main.index')
            return redirect(next_page)
        else:
            flash(message, 'danger')
            
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    """Çıkış yap."""
    logout_user()
    flash('Başarıyla çıkış yaptınız.', 'info')
    return redirect(url_for('main.index'))
