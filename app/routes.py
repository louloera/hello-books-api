from flask import Blueprint, jsonify, abort, make_response,request
from app import db 
from app.models.book import Book
from app.models.author import Author

books_bp = Blueprint ("books", __name__, url_prefix="/books")
authors_bp = Blueprint ("authors", __name__, url_prefix="/authors")


def validate_book(cls, book_id):
    
    try:
        book_id = int(book_id)
    except:
        abort(make_response(jsonify({"message":f"{cls.__name__} {book_id} invalid"}),400))
        #abort(make_response({"message":f"Book {book_id} invalid"},400))

    book = cls.query.get(book_id)

    if not book:
        abort(make_response({"message":f"{cls.__name__} {book_id} not found"},404))
        

    return book


@books_bp.route("", methods=[ "GET"])

def read_all_books():

    title_query = request.args.get("title")

    if title_query:
        books = Book.query.filter_by(title=title_query)
        
    else: 
    
        books = Book.query.all()
    
    books_response = []
    for book in books: 
        books_response.append(book.to_dict())
    
    return make_response(jsonify (books_response), 200)

@books_bp.route("", methods=["POST"])

def create_book():

    request_body = request.get_json()
    new_book = Book.from_dict(request_body)
    
    db.session.add(new_book)
    db.session.commit()

    return make_response (jsonify(f"Book {new_book.title} successfully created"),201)


@books_bp.route("/<book_id>" , methods= ["GET"])

def handle_book (book_id):

    book = validate_book(Book, book_id)

    if book == None:
        return make_response("", status=404)
    else:
        return book.to_dict()

@books_bp.route("/<book_id>" , methods= ["PUT"])

def update_book(book_id):

    book = validate_book(Book, book_id)

    request_body = request.get_json()

    book.title = request_body["title"]
    book.description = request_body["description"]

    db.session.commit()

    return make_response (jsonify(f"Book #{book.id} successfully updated",201))

@books_bp.route("/<book_id>", methods = ["DELETE"])
def delete_book(book_id):
    book= validate_book(Book, book_id)

    db.session.delete(book)
    db.session.commit()

    return make_response(jsonify(f"Book #{book.id} successfully deleted",200))

@authors_bp.route("", methods=[ "GET"])

def read_all_authors():

    authors = Author.query.all()
    
    authors_response = []
    for author in authors: 
        authors_response.append(author.to_dict())
    
    return make_response(jsonify (authors_response), 200)

@authors_bp.route("", methods=["POST"])

def create_author():

    request_body = request.get_json()
    new_author = Author.from_dict(request_body)
    
    db.session.add(new_author)
    db.session.commit()

    return make_response (jsonify(f"Author {new_author.name} successfully created"),201)


@authors_bp.route("/<author_id>/books", methods=[ "GET"])

def read_all_book_one_author(author_id):

    author= validate_book(Author, author_id)
    
    books_response = []
    for book in author.books: 
        books_response.append(book.to_dict())
    
    return make_response(jsonify (books_response), 200)

@authors_bp.route("/<author_id>/books", methods=["POST"])

def create_newbook_specific_author(author_id):

    author = validate_book(Author, author_id)

    request_body = request.get_json()
    new_book = Book.from_dict(request_body,author_id)
    
    db.session.add(new_book)
    db.session.commit()

    return make_response (jsonify(f"Book {new_book.title} by {new_book.author.name} successfully created"),201)

@authors_bp.route("/<author_id>" , methods= ["GET"])

def handle_book (author_id):

    author = validate_book(Author,author_id)

    if author == None:
        return make_response("", status=404)
    else:
        return author.to_dict()