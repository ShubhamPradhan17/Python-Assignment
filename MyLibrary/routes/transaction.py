from flask import *
from models import transactions, Books, Members
from datetime import *
from utils.decorator import role_required

transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('/issue', methods=['POST'])
@role_required('librarian')
def issue_book():
    data = request.json

    # current_user = get_jwt_identity()
    # if current_user['role'] != 'librarian':
    #     return jsonify({'msg': 'Access forbidden: Librarians only'})

    try:
        print(data)
        book_id = data['book_id']
        member_id = data['member_id']
        days_issued = data.get('days_issued', 7)

        
        book = Books.get(book_id)
        member = Members.get(member_id)

        if book.quantity < 1:
            return jsonify({'error': 'Book is out of stock'}), 400

        
        if member.debt > 500:
            return jsonify({'error': 'Member has outstanding debt greater than Rs. 500'}), 400

        
        transaction = transactions(
            book=book,
            member=member,
            date_submission=datetime.now() + timedelta(days=days_issued)
        )


        book.set(quantity=book.quantity - 1, issued_count=book.issued_count + 1)

        return jsonify({
            'message': f'Book "{book.book_name}" issued to {member.first_name} {member.last_name} for {days_issued} days',
            'transaction_id': transaction.id
        }), 201

    except Exception as e:
        return jsonify({'error': f'{e}'})
    

    

@transactions_bp.route('/return', methods=['POST'])
@role_required('librarian')
def return_book():
    data = request.json

    # current_user = get_jwt_identity()
    # print(current_user['user_id'])
    # if current_user['role'] != 'librarian':
    #     return jsonify({'msg': 'Access forbidden: Librarians only'})
    
    try:
        transaction_id = data['transaction_id']

        transaction = transactions.get(transaction_id)

        if transaction.return_status:
            return jsonify({'error': 'Book has already been returned'}), 400

        return_date = datetime.now()
        due_date = return_date - timedelta(seconds=30)

        transaction.set(date_submission=return_date, return_status=True)

        book = transaction.book
        book.set(quantity=book.quantity + 1, issued_count=book.issued_count - 1)

        fine_amount = 0.0
        if return_date > due_date:
            seconds_late = (return_date - due_date).seconds
            fine_amount = seconds_late * 10 

        member = transaction.member
        member.set(debt=member.debt + fine_amount)

        transaction.set(fine_amount=fine_amount)

        return jsonify({
            'message': f'Book "{book.book_name}" returned by {member.first_name} {member.last_name}',
            'fine_amount': fine_amount
        }), 200

    except Exception as e:
        return jsonify({'error': f'{e}'}), 400



