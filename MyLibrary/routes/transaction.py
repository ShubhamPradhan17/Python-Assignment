from flask import *
from models import transactions, Books, Members
from datetime import *
from utils.decorator import role_required
from sqlobject.sqlbuilder import AND


transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('/get_transactions', methods=['GET'])
@role_required('librarian')
def get_book():
    try: 
        transaction = transactions.select()

        result = [{'id': i.id , 'book' : i.book.book_name , 'member' : f"{i.member.first_name} {i.member.last_name}" ,
                    'date_issued' : i.date_issued , 'return_status': i.return_status , 'date_submission': i.date_submission, 'due_date' : i.due_date} for i in transaction]
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'msg' : f"{e}"})

@transactions_bp.route('/book_issue', methods=['POST'])
@role_required('librarian')
def issue_book():
    data = request.json

    # current_user = get_jwt_identity()
    # if current_user['role'] != 'librarian':
    #     return jsonify({'msg': 'Access forbidden: Librarians only'})

    try:
        if 'book_id' not in data or 'member_id' not in data:
            return jsonify({'error': 'Both book_id and member_id are required'}), 400
        
        book_id = data['book_id']
        member_id = data['member_id']
        days_issued = data.get('days_issued', 7)
        
        try:
            book = Books.get(book_id)
            member = Members.get(member_id)
        except Exception as e:
            return jsonify({'msg' : f'Error retrieving book or member: {str(e)}'}), 404


        if book.quantity < 1:
            return jsonify({'error': 'Book is out of stock'}), 400

        
        if member.debt > 500:
            return jsonify({'error': 'Member has outstanding debt greater than Rs. 500'}), 400

        
        transaction = transactions(
            book=book,
            member=member,
            due_date=datetime.now() + timedelta(days=days_issued),
        )


        book.set(quantity=book.quantity - 1, issued_count=book.issued_count + 1)

        return jsonify({
            'message': f'Book "{book.book_name}" issued to {member.first_name} {member.last_name} for {days_issued} days',
            'transaction_id': transaction.id
        }), 201

    except ValueError:
        return jsonify({'error': 'Invalid input provided'}), 400
    
    except Exception as e:
        return jsonify({'error': f'{e}'})
    

    

@transactions_bp.route('/book_return', methods=['POST'])
@role_required('librarian')
def return_book():
    
    data = request.json

    # current_user = get_jwt_identity()
    # print(current_user['user_id'])
    # if current_user['role'] != 'librarian':
    #     return jsonify({'msg': 'Access forbidden: Librarians only'})
    
    try:
        if 'transaction_id' not in data:
            return jsonify({'error': 'transaction_id is required'}), 400
        
        transaction_id = data['transaction_id']

        try:
            transaction = transactions.get(transaction_id)
        except Exception as e:
             return jsonify({'error': f'Transaction not found: {e}'}), 404

        if transaction.return_status:
            return jsonify({'error': 'Book has already been returned'}), 400

        return_date = datetime.now() + timedelta(days=0)
        due_date = transaction.due_date

        transaction.set(date_submission=return_date, return_status=True)

        book = transaction.book
        book.set(quantity=book.quantity + 1, issued_count=book.issued_count - 1)

        fine_amount = 0.0
        if return_date > due_date:
            days_late = (return_date - due_date).days
            fine_amount = days_late * 10 

        
        member = transaction.member
        member.set(debt=member.debt + fine_amount)

        transaction.set(fine_amount=fine_amount)

        return jsonify({
            'message': f'Book "{book.book_name}" returned by {member.first_name} {member.last_name}',
            'fine_amount': fine_amount
        }), 200

    except ValueError:
        return jsonify({'error': 'Invalid input provided'}), 400
    except Exception as e:
        return jsonify({'error': f'{e}'}), 400



@transactions_bp.route('/overdue_report', methods=['GET'])
@role_required('librarian') 
def overdue_report():
    try:
        current_time = datetime.now()
        new_time = current_time   + timedelta(days=9)

        print(f"Current UTC time: {new_time}")

        overdue_transactions = transactions.select(
            AND(transactions.q.due_date < new_time,
                transactions.q.return_status == False)
        )

        overdue_list = []
        for transaction in overdue_transactions:
            member = transaction.member
            book = transaction.book
            days_overdue = (new_time - transaction.due_date).days

            print(days_overdue, member.first_name, book.book_name)

            fine = days_overdue * 10 if days_overdue > 0 else 0

            overdue_list.append({
                'transaction_id': transaction.id,
                'book_name': book.book_name,
                'member_name': f'{member.first_name} {member.last_name}',
                'due_date': transaction.due_date.strftime('%Y-%m-%d'),
                'days_overdue': days_overdue,
                'fine': fine
            })

        return jsonify({'overdue_transactions': overdue_list}), 200
    except Exception as e:
        return jsonify({'error': f"Unexpected error: {e}"}), 500
