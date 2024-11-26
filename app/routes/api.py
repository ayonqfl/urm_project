from datetime import datetime, timezone
from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from flask_login import current_user, login_required

from app import db
from ..models import Roles

api = Blueprint('api', __name__, template_folder='templates', static_folder='static')

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
        return jsonify({'error': 'Internal server error!'}), 400
    


@api.route('/roles_api_list', methods=['GET'])
@login_required
def roles_api_list():
    try:
        all_roles = Roles.query.order_by(Roles.id.desc()).all()

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
        return jsonify({'error': 'Internal server error!'}), 400
    
    