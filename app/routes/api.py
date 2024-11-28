from datetime import datetime, timezone
from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError

from app import db
from ..models import Roles, RolesAPI, Users, UsersRole

api = Blueprint('api', __name__, template_folder='templates', static_folder='static')


# --- helper functions ---
@api.route('/autocompleteRoles', methods=['GET'])
@login_required
def autocomplete():
    query = request.args.get('query', '')
    if query:
        suggestions = db.session.query(Roles.role_name).filter(Roles.role_name.ilike(f'%{query}%')).limit(10).all()
        suggestions_list = [role[0] for role in suggestions]
        return jsonify(suggestions_list), 200
    return jsonify([]), 200


@api.route('/userRoles', methods=['GET'])
@login_required
def user_roles():
    query = request.args.get('query', '').strip()
    if query:
        suggestions = (
            db.session.query(Roles.role_name)
            .filter(Roles.role_name.ilike(f'%{query}%'))
            .limit(10)
            .all()
        )
    else:
        suggestions = db.session.query(Roles.role_name).limit(10).all()

    suggestions_list = [role_name for (role_name,) in suggestions]
    return jsonify(suggestions_list), 200


# --- api users functions ---
@api.route('/create_api_user', methods=['POST'])
@login_required
def create_api_user():
    data = request.get_json()

    username = data.get('username', None)
    user_type = data.get('user_type', None)
    password = data.get('password', None)
    confirmPassword = data.get('confirmPassword', None)
    roles = data.get('roles', [])

    if not username or not user_type or not password or not roles:
        return jsonify({'error': 'Username, type, password, and roles are required fields.'}), 406
    
    if Users.query.filter(Users.username == username).first():
        return jsonify({'error': 'Username already exists'}), 406

    if password != confirmPassword:
        return jsonify({'error': 'Passwords do not match.'}), 406

    # Check if the roles exist in the Roles table
    role_objects = Roles.query.filter(Roles.role_name.in_(roles)).all()
    if len(role_objects) != len(roles):
        return jsonify({'error': 'One or more roles are invalid.'}), 400

    # Create the user
    hashed_password = generate_password_hash(password)
    new_user = Users(
        username=username,
        type=user_type,
        password=hashed_password,
        email=data.get('email', None) or None,
        phone=data.get('phone', None) or None,
        details=data.get('details', None) or None,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )

    try:
        db.session.add(new_user)
        db.session.commit()

        # Save roles in UsersRole
        for role in role_objects:
            user_role = UsersRole(
                user_id=new_user.id,
                role_id=role.id,
                username=username,
                role_name=role.role_name,
                created_at=datetime.now(timezone.utc)
            )
            db.session.add(user_role)
        db.session.commit()

        return jsonify({'success': 'API User created successfully!'}), 201
    except IntegrityError as ex:
        db.session.rollback()
        print("Error:", str(ex))
        return jsonify({'error': 'Internal server error, duplicate entry or invalid data.'}), 500
    except Exception as ex:
        print("Error: ", str(ex))
        db.session.rollback() 
        return jsonify({'error': 'Internal server error!'}), 500


@api.route('/api_user_list', methods=['GET'])
@login_required
def api_user_list():
    username = request.args.get('username', None)
    user_type = request.args.get('user_type', None)

    try:
        query = (
            db.session.query(Users, UsersRole.role_name)
            .join(UsersRole, Users.id == UsersRole.user_id, isouter=True)
            .filter(Users.type != 'Admin')
        )

        if username:
            query = query.filter(Users.username.ilike(f'%{username}%'))
        if user_type:
            query = query.filter(Users.type == user_type)

        users_with_roles = query.order_by(Users.id.desc()).all()

        users_data = {}
        for user, role_name in users_with_roles:
            if user.id not in users_data:
                users_data[user.id] = {
                    "id": user.id,
                    "username": user.username,
                    "type": user.type,
                    "email": user.email,
                    "phone": user.phone,
                    "details": user.details,
                    "created_at": user.created_at.strftime('%d-%m-%Y'),
                    "updated_at": user.updated_at.strftime('%d-%m-%Y'),
                    "roles": [],
                }
            if role_name:
                users_data[user.id]["roles"].append(role_name)

        return jsonify(list(users_data.values())), 200

    except Exception as ex:
        print("Error: ", str(ex))
        return jsonify({'error': 'Internal server error!'}), 500


@api.route('/delete_api_user', methods=['DELETE'])
@login_required
def delete_api_user():
    user_id = request.args.get('user_id', None)
    if not user_id:
        return jsonify({'error': 'User ID is required!'}), 400

    try:
        user = Users.query.get(user_id)
        print(user)
        if not user:
            return jsonify({'error': 'User not found!'}), 404

        db.session.delete(user)
        db.session.commit()
        return jsonify({'success': f'API with ID {user.username} has been deleted successfully!'}), 200

    except Exception as ex:
        print("Error: ", str(ex))
        db.session.rollback()
        return jsonify({'error': 'Internal server error!'}), 500



# --- postman api for api user role, roles-api's data & authentication functionality ---
@api.route('/users_roles_apis_data', methods=['GET'])
def users_roles_apis_data():
    user_id = 14
    username = 'gregory_api'
    try:
        user = Users.query.filter_by(id=user_id, username=username).first()

        if not user:
            return jsonify({'error': 'User not found!'}), 404

        # Fetch user roles
        user_roles = (
            db.session.query(UsersRole.role_name)
            .filter_by(user_id=user.id)
            .all()
        )
        role_names = [role.role_name for role in user_roles]

        # Fetch APIs associated with the user's roles
        apis = (
            db.session.query(RolesAPI)
            .join(Roles, RolesAPI.role_id == Roles.id)
            .filter(Roles.role_name.in_(role_names))
            .all()
        )

        api_data = [
            {
                "role": api.role_name,
                "api": api.api,
                "api_type": api.type,
                "api_details": api.details,
            }
            for api in apis
        ]

        response_data = {
            "user": {
                "id": user.id,
                "username": user.username,
                "user_type": user.type,
            },
            "user_roles": role_names,
            "user_role_apis": api_data,
        }
        return jsonify(response_data), 200
    except Exception as ex:
        print("Error: ", str(ex))
        return jsonify({'error': 'Internal server error!'}), 500



# --- roles & api's functions ---
@api.route('/create_role_name', methods=['GET'])
@login_required
def create_role_name():
    role_name = request.args.get('role_name', None)
    if not role_name:
        return jsonify({'error': 'Role Name field is required!'}), 406
    
    try:
        is_exist_role = Roles.query.filter_by(role_name=role_name).first()
        if is_exist_role:
            return jsonify({'error': 'Role Name already exists!'}), 406
        else:
            create_role = Roles(
                role_name=role_name,
                created_by=current_user.username,
                created_at=datetime.now(timezone.utc)
            )
            db.session.add(create_role)
            db.session.commit()
            return jsonify({'success': 'Role created successfully!'}), 201
    except Exception as ex:
        print("Error: ", str(ex))
        db.session.rollback() 
        return jsonify({'error': 'Internal server error!'}), 500
    


@api.route('/roles_list', methods=['GET'])
@login_required
def roles_list():
    role_name = request.args.get('role_name', None)
    created_by = request.args.get('created_by', None)

    try:
        query = Roles.query

        if role_name:
            query = query.filter(Roles.role_name.ilike(f'%{role_name}%'))
        if created_by:
            query = query.filter(Roles.created_by.ilike(f'%{created_by}%'))

        all_roles = query.order_by(Roles.id.desc()).all()

        roles_list = [
            {
                'id': role.id,
                'role_name': role.role_name,
                'created_by': role.created_by,
                'created_at': role.created_at.strftime('%d-%m-%Y')
            } for role in all_roles
        ]
        return jsonify(roles_list), 200
    except Exception as ex:
        print("Error: ", str(ex))
        return jsonify({'error': 'Internal server error!'}), 500
    


@api.route('/delete_role', methods=['DELETE'])
@login_required
def delete_role():
    role_id = request.args.get('role_id', None)

    if not role_id:
        return jsonify({'error': 'Role ID is required!'}), 400

    try:
        role = Roles.query.get(role_id)
        if not role:
            return jsonify({'error': 'Role not found!'}), 404

        db.session.delete(role)
        db.session.commit()

        return jsonify({'success': f'Role with ID {role.role_name} has been deleted successfully!'}), 200

    except Exception as ex:
        print("Error: ", str(ex))
        db.session.rollback()
        return jsonify({'error': 'Internal server error!'}), 500



@api.route('/create_api')
@login_required
def create_api():
    api_role = request.args.get('api_role', None)
    api_type = request.args.get('api_type', None)
    api_link = request.args.get('api_link', None)
    api_details = request.args.get('api_details', None)

    # print(api_role, api_type, api_link)

    if not api_role:
        return jsonify({'error': 'Role field is required!'}), 406
    
    if not api_type:
        return jsonify({'error': 'Type field is required!'}), 406
    
    if not api_link:
        return jsonify({'error': 'API Link field is required!'}), 406
    
    try:
        role = Roles.query.filter_by(role_name=api_role).first()
        if not role:
            return jsonify({'error': f"Role '{api_role}' not found!"}), 404
        
        existing_api = RolesAPI.query.filter_by(role_id=role.id, api=api_link, type=api_type).first()
        if existing_api:
            return jsonify({'error': 'API with the same link and type already exists for this role!'}), 409
        
        new_api = RolesAPI(
            role_id=role.id,
            role_name=role.role_name,
            api=api_link,
            type=api_type,
            details=api_details
        )
        
        db.session.add(new_api)
        db.session.commit()

        return jsonify({'success': 'API created successfully!'}), 201
    except Exception as ex:
        print("Error: ", str(ex))
        return jsonify({'error': 'Internal server error!'}), 500
    


@api.route('/api_list')
@login_required
def api_list():
    api_role = request.args.get('api_role', None)
    api_type = request.args.get('api_type', None)
    api_link = request.args.get('api_link', None)

    print(api_role, api_type, api_link)

    try:
        query = RolesAPI.query
        if api_role:
            query = query.filter(RolesAPI.role_name.ilike(f"%{api_role}%"))
        if api_type:
            query = query.filter(RolesAPI.type == api_type)
        if api_link:
            query = query.filter(RolesAPI.api.ilike(f"%{api_link}%"))

        all_apies = query.order_by(RolesAPI.id.desc()).all()
        all_apies = [api.to_dict() for api in all_apies]
        return jsonify(all_apies), 200
    except Exception as ex:
        print("Error: ", str(ex))
        return jsonify({'error': 'Internal server error!'}), 500
    

@api.route('/delete_api', methods=['DELETE'])
@login_required
def delete_api():
    role_id = request.args.get('api_id', None)

    if not role_id:
        return jsonify({'error': 'Role ID is required!'}), 400

    try:
        api = RolesAPI.query.get(role_id)
        if not api:
            return jsonify({'error': 'Role not found!'}), 404

        db.session.delete(api)
        db.session.commit()

        return jsonify({'success': f'API with ID {api.role_name}, {api.type} has been deleted successfully!'}), 200

    except Exception as ex:
        print("Error: ", str(ex))
        db.session.rollback()
        return jsonify({'error': 'Internal server error!'}), 500