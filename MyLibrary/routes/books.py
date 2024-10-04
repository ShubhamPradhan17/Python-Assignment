from flask import *
from models import Books
from sqlobject import AND
from utils.decorator import role_required
from dotenv import load_dotenv
import os
from datetime import *

books_bp = Blueprint('books', __name__)

@books_bp.route('/create_books', methods=['POST'])
@role_required('librarian')
def create_book():

    # current_user = get_jwt_identity()
    # if current_user['role'] != 'librarian':
    #     return jsonify({'msg': 'Access forbidden: Librarians only'}), 403
    
    try: 
        data = request.json

        if 'book_name' not in data or not data['book_name']:
            return jsonify({'message': 'Book name is required'}), 400
        
        if 'author' not in data or not data['author']:
            return jsonify({'message': 'Author name is required'}), 400

        if 'isbn' not in data or not isinstance(data['isbn'], str):
            return jsonify({'message': 'ISBN is required and must be a string'}), 400
        
        if 'quantity' in data:
            if not isinstance(data['quantity'], int) or data['quantity'] < 0:
                return jsonify({'message': 'Quantity must be a non-negative integer'}), 400
        
        if 'genre' in data and not isinstance(data['genre'], str):
            return jsonify({'message': 'Genre must be a string'}), 400
        
        existing_book = Books.selectBy(book_name=data['book_name']).count() > 0 or Books.selectBy(isbn=data['isbn']).count() > 0
                        
        if existing_book:
            return jsonify({'message': 'Book with the same name or ISBN already exists'}), 400

        date_updated = datetime.now()
        
        book = Books(
            book_name = data['book_name'],
            author = data['author'],
            publisher = data['publisher'],
            quantity = 20,
            issued_count = data.get('issued_count', 0),
            genre = data['genre'],
            isbn = data['isbn'],
            date_updated = date_updated
        )


        return jsonify({'id': book.id, 'message': 'Book created successfully!'}),201

    except Exception as e:
        return jsonify({'msg': f"Unexpected Error: {e}"}),500


@books_bp.route('/get_books' , methods = ['GET'])
def get_books():
    try:
        
        page_size = os.getenv('PAGE_SIZE')
    
        try:
            page = int(request.args.get('page',1))
            per_page = int(request.args.get('per_page', page_size))
        except ValueError as e:
            return jsonify({'msg' : "Invalid page or per_page value"}), 400

        start = (page - 1) * per_page
        end = start + per_page
        
        

        result = [{'id': book.id, 'book_name': book.book_name, 'author': book.author, 'publisher': book.publisher,
                 'isbn': book.isbn, 'quantity': book.quantity, 'issued_count': book.issued_count, 'genre': book.genre}
                  for book in books]
        return jsonify(result),200
    
    except Exception as e:
        return jsonify({'message': f"{e}"}),400


@books_bp.route('/get_books/<int:book_id>', methods = ['GET'])
def get_book(book_id):
    try:
        try:
            book = Books.get(book_id)
        except Exception as db_error:
            return jsonify({'msg': f"Error occured : {db_error}"}), 500
        
        result = {'id': book.id, 'book_name': book.book_name, 'author': book.author, 'publisher': book.publisher,
               'isbn': book.isbn, 'quantity': book.quantity, 'issued_count': book.issued_count, 'genre': book.genre}
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'message':f"{e}"}), 404
    


@books_bp.route('/update_books/<int:book_id>', methods= ['PUT'])
@role_required('librarian')
def update_book(book_id):
    
    # current_user = get_jwt_identity()
    # if current_user['role'] != 'librarian':
    #     return jsonify({'msg': 'Access forbidden: Librarians only'}), 403
    
    data = request.json
    try: 
        book = Books.get(book_id)
        
        if 'book_name' not in data or not data['book_name']:
            return jsonify({'message': 'Book name is required'}), 400
        
        if 'author' not in data or not data['author']:
            return jsonify({'message': 'Author name is required'}), 400

        if 'isbn' not in data or not isinstance(data['isbn'], str):
            return jsonify({'message': 'ISBN is required and must be a string'}), 400
        
        if 'quantity' in data:
            if not isinstance(data['quantity'], int) or data['quantity'] < 0:
                return jsonify({'message': 'Quantity must be a non-negative integer'}), 400
        
        if 'issued_count' in data:
            if not isinstance(data['issued_count'], int) or data['issued_count'] < 0:
                return jsonify({'message': 'Issued count must be a non-negative integer'}), 400
        
        if 'genre' in data and not isinstance(data['genre'], str):
            return jsonify({'message': 'Genre must be a string'}), 400

        date_updated = datetime.now()

        book.set(
            book_name = data['book_name'],
            author=data['author'],
            publisher=data.get('publisher', book.publisher),
            isbn=data['isbn'],
            quantity=data['quantity'],
            issued_count=data.get('issued_count', book.issued_count),
            genre=data.get('genre', book.genre),
            date_updated = date_updated
        )
        
        return jsonify({'message':'Book updated Successfully!'}), 200
    except Exception as e:
        return jsonify({'message':f"{e}"}), 404


@books_bp.route('/delete_books/<int:book_id>' , methods = ['DELETE'])
@role_required('librarian')
def delete_book(book_id):

    # current_user = get_jwt_identity()
    # if current_user['role'] != 'librarian':
    #     return jsonify({'msg': 'Access forbidden: Librarians only'}), 403

    try:
        book = Books.get(book_id)

        if not book:
            return jsonify({'msg' : "Book ID not found"}), 404
        
        book.destroySelf()
        return jsonify({'message' : "The book is Deleted Successfully"}), 200
    
    except Exception as e:
        return jsonify({'message' : f"{e}"})
    


@books_bp.route('/search' , methods = ["GET"])
def search_book():
    title = request.args.get('title', '')
    author = request.args.get('author', '')
    isbn = request.args.get('isbn', '')

    filters = []
    if title:
        filters.append(Books.q.book_name.contains(title))
    if author:
        filters.append(Books.q.author.contains(author))
    if isbn:
        filters.append(Books.q.isbn == isbn)

    print(filters)
    
    if filters:
        combined_filters = AND(*filters)
        print(combined_filters)
        books = Books.select(combined_filters).orderBy(Books.q.id)
    else:
        books = Books.select().orderBy(Books.q.id)
    
    book_list = [{
        'id': book.id,
        'title': book.book_name,
        'author': book.author,
        'publisher': book.publisher,
        'quantity': book.quantity,
        'issued_count': book.issued_count,
        'isbn' : book.isbn
    } for book in books]

    return jsonify(book_list), 200