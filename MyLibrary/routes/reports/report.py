from flask import Blueprint, jsonify
from models import Books, transactions
from utils.decorator import role_required
from sqlobject.sqlbuilder import *

report_bp = Blueprint('report', __name__)

@report_bp.route('/reports/popular-books', methods=['GET'])
@role_required('librarian')
def get_popular_books():
    # Perform the query
    query = Books.select(orderBy=DESC(Books.q.issued_count))
    
    # Execute the query and fetch results
    results = query

    popular_books = []
    print(results)
    for row in query:
        book = Books.get(row.id)  # Fetch book details from Books table
        available_stock = 20 - book.issued_count
        print(book.quantity, book.issued_count, available_stock)
        
        popular_books.append({
            'book_name': book.book_name,
            'author': book.author,
            'issued_count': book.issued_count,
            'available_stock': available_stock
        })

    return jsonify(popular_books), 200



