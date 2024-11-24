from datetime import datetime, timezone
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app import login_manager
from ..models import Users

shared = Blueprint('shared', __name__, template_folder='templates', static_folder='static')

@login_manager.user_loader
def load_user(uid):
    user = Users.query.get(int(uid))
    return user

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('shared.admin_signin_view'))

@shared.route('/')
@login_required
def dashboard_view():
    if current_user.is_authenticated:
        return render_template('users/dashboard.html')
    else:
        return redirect(url_for('shared.admin_signin_view'))

@shared.route('/signup', methods=['GET', 'POST'])
def admin_signup_view():
    if request.method == 'GET':
        return render_template('users/signup.html')

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        user_type = request.form.get('type')
        details = request.form.get('details')

        if not username or not email or not password or not user_type:
            flash("All fields are required", 'error')
            return redirect(url_for('shared.admin_signup_view'))

        if user_type not in ['Admin', 'API']:
            flash("Invalid user type", 'error')
            return redirect(url_for('shared.admin_signup_view'))

        if Users.query.filter((Users.username == username) | (Users.email == email)).first():
            flash("Username or email already exists", 'error')
            return redirect(url_for('shared.admin_signup_view'))

        hashed_password = generate_password_hash(password)
        new_user = Users(
            username=username,
            email=email,
            password=hashed_password,
            type=user_type,
            details=details,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('shared.admin_signin_view'))



@shared.route('/signin', methods=['GET', 'POST'])
def admin_signin_view():
    if request.method == 'GET':
        return render_template('users/signin.html')
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = Users.query.filter(Users.username == username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('shared.dashboard_view'))

        else:
            flash("Faild to sign up", 'error')
            return redirect(url_for('shared.admin_signin_view'))



@shared.route('/signout')
def signout_view():
    logout_user()
    return redirect(url_for('shared.admin_signin_view'))

        
