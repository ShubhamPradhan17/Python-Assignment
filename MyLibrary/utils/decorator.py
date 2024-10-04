from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify

def role_required(*roles):
    def verify_role(func):
        @wraps(func)
        @jwt_required()
        def wrapper_func(*args, **kwargs):
            
            current_user = get_jwt_identity() 
            member_id = kwargs.get('member_id', None)

            if roles and current_user['role'] not in roles:
                return jsonify({'message': "Forbidden"}), 403
            
      
            if member_id:
                if current_user['role'] != 'librarian':
                    if current_user['user_id'] != member_id:
                        return jsonify({'message': "Forbidden."}), 403
                
            return func(*args, **kwargs)
        
        return wrapper_func
    return verify_role


                



