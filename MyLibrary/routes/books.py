from flask import *
from models import Books
from sqlobject import AND
from utils.decorator import role_required

books_bp = Blueprint('books', __name__)

@books_bp.route('/books', methods=['POST'])
@role_required('librarian')
def create_book():

    # current_user = get_jwt_identity()
    # if current_user['role'] != 'librarian':
    #     return jsonify({'msg': 'Access forbidden: Librarians only'}), 403
    
    try: 
        data = request.json
        print(data)
        book = Books(
            book_name = data['book_name'],
            author = data['author'],
            publisher = data['publisher'],
            quantity = 20,
            issued_count = data.get('issued_count', 0),
            genre = data['genre'],
            isbn = data['isbn']
        )
        return jsonify({'id': book.id, 'message': 'Book created successfully!'}),201

    except Exception as e:
        print(e)

@books_bp.route('/books' , methods = ['GET'])
def get_books():
    try:
        books = Books.select().orderBy(Books.q.id)
        result = [{'id': book.id, 'book_name': book.book_name, 'author': book.author, 'publisher': book.publisher,
                'isbn': book.isbn, 'quantity': book.quantity, 'issued_count': book.issued_count, 'genre': book.genre}
                for book in books]
        return jsonify(result),200
    except Exception as e:
        return jsonify({'message': f"{e}"})


@books_bp.route('/books/<int:book_id>', methods = ['GET'])
def get_book(book_id):
    try:
        book = Books.get(book_id)
        result = {'id': book.id, 'book_name': book.book_name, 'author': book.author, 'publisher': book.publisher,
               'isbn': book.isbn, 'quantity': book.quantity, 'issued_count': book.issued_count, 'genre': book.genre}
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'message':f"{e}"}), 404
    


@books_bp.route('/books/<int:book_id>', methods= ['PUT'])
@role_required('librarian')
def update_book(book_id):
    
    # current_user = get_jwt_identity()
    # if current_user['role'] != 'librarian':
    #     return jsonify({'msg': 'Access forbidden: Librarians only'}), 403
    
    data = request.json
    try: 
        book = Books.get(book_id)
        book.set(
            book_name = data['book_name'],
            author=data['author'],
            publisher=data.get('publisher'),
            isbn=data['isbn'],
            quantity=data['quantity'],
            issued_count=data.get('issued_count', book.issued_count),
            genre=data.get('genre', book.genre)
        )
        return jsonify({'message':'Book updated Successfully!'}), 200
    except Exception as e:
        return jsonify({'message':f"{e}"}), 404


@books_bp.route('/books/<int:book_id>' , methods = ['DELETE'])
@role_required('librarian')
def delete_book(book_id):

    # current_user = get_jwt_identity()
    # if current_user['role'] != 'librarian':
    #     return jsonify({'msg': 'Access forbidden: Librarians only'}), 403
    
    book = Books.get(book_id)
    try:
        book.destroySelf()
        return jsonify({'message' : "The book is Deleted Successfully"})
    except Exception as e:
        return jsonify({'message' : f"{e}"})
    


@books_bp.route('/search' , methods = ["GET"])
def search_book():
    title = request.args.get('title', '')
    author = request.args.get('author', '')
    isbn = request.args.get('isbn', '')

    print(title,author)
    filters = []
    if title:
        filters.append(Books.q.book_name.contains(title))
    if author:
        filters.append(Books.q.author.contains(author))
    if isbn:
        filters.append(Books.q.isbn == isbn)

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