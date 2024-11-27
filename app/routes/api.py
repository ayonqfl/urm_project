from datetime import datetime, timezone
from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from flask_login import current_user, login_required

from app import db
from ..models import Roles, RolesAPI

api = Blueprint('api', __name__, template_folder='templates', static_folder='static')


# --- autocomplete helper functions ---
@api.route('/autocompleteRoles', methods=['GET'])
@login_required
def autocomplete():
    query = request.args.get('query', '')
    if query:
        suggestions = db.session.query(Roles.role_name).filter(Roles.role_name.ilike(f'%{query}%')).all()
        suggestions_list = [role[0] for role in suggestions]
        return jsonify(suggestions_list), 200
    return jsonify([]), 200


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