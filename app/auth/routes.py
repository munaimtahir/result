"""
Authentication routes
"""

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from app.auth import bp
from app.forms import LoginForm
from app.models import User

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login page"""
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash('Logged in successfully!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('admin.dashboard'))
        flash('Invalid username or password', 'danger')
    
    return render_template('auth/login.html', title='Admin Login', form=form)

@bp.route('/logout')
def logout():
    """Logout admin user"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))