from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Members
from utils.auth import verify_password, generate_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'msg': 'Email and password required'}), 400

    user = Members.selectBy(email=email).getOne(None)
    
    if user is None or verify_password(user.password, password) != True:
        return jsonify({'msg': 'Invalid email or password'}), 401

    token = generate_token(user.id, user.role)
    return jsonify({'token': token})


# @auth_bp.route('/protected', methods=['GET'])
# @jwt_required()
# def protected():
#     current_user = get_jwt_identity()
#     return jsonify(logged_in_as=current_user), 200
