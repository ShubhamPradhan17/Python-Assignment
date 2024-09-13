from flask import *
from models import Members
from utils.auth import hash_password
from utils.decorator import role_required

members_bp = Blueprint('Members', __name__)

@members_bp.route('/member', methods=['POST'])
@role_required('librarian')
def create_member():
    
    # current_user = get_jwt_identity()
    # if current_user['role'] != 'librarian':
    #     return jsonify({'msg': 'Access forbidden: Librarians only'}), 403

    try: 
        data = request.json
        hashed_password = hash_password(data.get('password'))

        member = Members(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            phone_no=data['phone'],
            address=data.get('address'),
            debt=data.get('debt', 0.0),
            password=hashed_password
        )
        return jsonify({'id': member.id ,
                        'Name': member.first_name,
                        "Password": data.get('password'),                    
                        'message': 'Member created successfully!'}),201

    except Exception as e:
        return jsonify({'message': f"{e}"}),400


@members_bp.route('/member' , methods=['GET'])
@role_required('librarian')
def get_members():
    # current_user = get_jwt_identity()
    # print(current_user)
    # if current_user['role'] != 'librarian':
    #     return jsonify({'msg': 'Access forbidden: Librarians only'}),403

    try:
        members = Members.select().orderBy(Members.q.id)
        result = [{'id': member.id, 'first_name': member.first_name, 'last_name': member.last_name, 'email': member.email,
                   'phone': member.phone_no, 'address': member.address, 'debt': member.debt, 'role': member.role}
                   for member in members]        
        return jsonify(result),200
    
    except Exception as e:
        return jsonify({'message': f"{e}"}),400
    

@members_bp.route('/member/<int:member_id>', methods = ["GET"])
@role_required()
def get_member(member_id):
    # current_user = get_jwt_identity()

    # print(current_user)
    # if current_user['user_id'] != member_id:
    #     return jsonify({'message': "Not allowed see other member"}),401
    
    # current_user = get_jwt_identity()
    # if current_user['role'] != 'librarian':
    #     return jsonify({'msg': 'Access forbidden: Librarians only'}), 403
    
    try:
        member = Members.get(member_id)
        result = {'id': member.id, 'first_name': member.first_name, 'last_name': member.last_name, 'email': member.email,
                   'phone': member.phone_no, 'address': member.address, 'debt': member.debt}
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'message':f"{e}"}), 400
    
    
@members_bp.route('/member/<int:member_id>', methods = ['PUT'])
@role_required()
def update_member(member_id):
    data = request.json

    # current_user = get_jwt_identity()

    # print(current_user)
    # if current_user['user_id'] != member_id:
    #     return jsonify({'message': "Not allowed to change other member details"}),401
    
    try:
        member = Members.get(member_id)

        member.set(
            first_name =  data['first_name'],
            last_name = data['last_name'], 
            email = data['email'],
            phone_no = data['phone_no'], 
            address = data['address'],
        )

        return jsonify({'message': "User detail updated successfully"}), 201
    
    except Exception as e:
        return jsonify(f"{e}"),400


@members_bp.route('/member/<int:member_id>', methods= ['DELETE'])
@role_required('librarian')
def delete_member(member_id):

    # current_user = get_jwt_identity()
    # if current_user['role'] != 'librarian':
    #     return jsonify({'msg': 'Access forbidden: Librarians only'}), 403
    
    member = Members.get(member_id)

    try:
        member.destroySelf()
        return jsonify({'message' : "The Member is Deleted Successfully"}),
    except Exception as e:
        return jsonify({'message' : f"{e}"})
    


@members_bp.route('/repay_debt', methods = ['POST'])
@role_required('librarian')
def repay_debt():
    data = request.json

    # current_user = get_jwt_identity()

    # if current_user['user_id'] != member_id:
    #     return jsonify({'message': "Not allowed to pay other members debt"}),401

    try:
        member_id = data['member_id']
        amount = float(data['amount'])

        member = Members.get(member_id)

        if amount <= 0:
            return jsonify({'error': 'Payment amount must be positive'}), 400

        if member.debt < amount:
            return jsonify({'error': 'Payment amount exceeds the current debt'}), 400

        new_debt = member.debt - amount
        member.set(debt=new_debt)

        return jsonify({
            'message': 'Debt repaid successfully',
            'new_debt': new_debt
        }), 201

    except Exception as e:
        return jsonify({'error': f"{e}"}), 400
    
