from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify

def role_required(*roles):
    def verify_role(func):
        @wraps(func)
        @jwt_required()  # Ensures JWT authentication
        def wrapper_func(*args, **kwargs):
            
            current_user = get_jwt_identity()  # Get the identity of the current user from the JWT token
            member_id = kwargs.get('member_id', None)

            # Check if the current user's role is allowed
            if roles and current_user['role'] not in roles:
                return jsonify({'message': "Forbidden"}), 403
            
            # Check if the current user is trying to access their own data
            if member_id:
                if current_user['role'] != 'librarian':
                    if current_user['user_id'] != member_id:
                        print(current_user['user_id'], member_id)
                        return jsonify({'message': "Forbidden."}), 403
                
            return func(*args, **kwargs)
        
        return wrapper_func
    return verify_role


                



