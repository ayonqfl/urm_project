from datetime import datetime, timezone
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app import login_manager
from ..models import Users, Roles

shared = Blueprint('shared', __name__, template_folder='templates', static_folder='static')

@login_manager.user_loader
def load_user(uid):
    user = Users.query.get(int(uid))
    return user

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('shared.signin_view'))

@shared.route('/')
@login_required
def dashboard_view():
    if current_user.is_authenticated:
        return render_template('users/dashboard.html')
    else:
        return redirect(url_for('shared.signin_view'))


@shared.route('/create_account', methods=['GET', 'POST'])
def create_account():
    return render_template('users/createaccount.html')

@shared.route('/user_list', methods=['GET', 'POST'])
def user_list():
    return render_template('users/accountlist.html')

@shared.route('/create_roles', methods=['GET', 'POST'])
@login_required
def create_roles():
    return render_template('users/createroles.html')

@shared.route('/assign_user_roles', methods=['GET', 'POST'])
def assign_user_roles():
    return render_template('users/assignroles.html')

@shared.route('/create_api', methods=['GET', 'POST'])
def create_api():
    return render_template('users/createapi.html')

@shared.route('/api_list', methods=['GET', 'POST'])
def api_list():
    return render_template('users/apilist.html')


@shared.route('/create_superuser', methods=['POST'])
def create_superuser():
    data = request.get_json()
    print(data)

    if not data:
        return jsonify({'error': 'Missing JSON data'}), 400

    username = data.get('username')
    password = data.get('password')
    user_type = data.get('type')
    email = data.get('email') if data.get('email') else None
    phone = data.get('phone') if data.get('phone') else None

    if not username or not password or not user_type:
        return jsonify({'error': 'All fields are required'}), 400

    if user_type != 'Admin':
        return jsonify({'error': 'Invalid superuser type'}), 400

    if Users.query.filter(Users.username == username).first():
        return jsonify({'error': 'Username already exists'}), 409

    hashed_password = generate_password_hash(password)
    new_user = Users(
        username=username,
        password=hashed_password,
        type=user_type,
        email=email,
        phone = phone,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201




@shared.route('/signin', methods=['GET', 'POST'])
def signin_view():
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
            flash("Invalid username or password, please try again!", 'error')
            return redirect(url_for('shared.signin_view'))



@shared.route('/signout')
def signout_view():
    logout_user()
    return redirect(url_for('shared.signin_view'))

        
