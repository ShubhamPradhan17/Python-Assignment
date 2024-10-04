from flask import Blueprint, jsonify
from models import Books, transactions
from utils.decorator import role_required
from sqlobject.sqlbuilder import *

report_bp = Blueprint('report', __name__)

@report_bp.route('/reports/popular-books', methods=['GET'])
@role_required('librarian')
def get_popular_books():

    query = Books.select(orderBy=DESC(Books.q.issued_count))

    popular_books = []

    for row in query:
        
        available_stock = row.quantity
        
        popular_books.append({
            'book_name': row.book_name,
            'author': row.author,
            'issued_count': row.issued_count,
            'available_stock': available_stock
        })

    return jsonify(popular_books), 200



