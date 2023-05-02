from flask import Blueprint, jsonify, abort, make_response,request
from app import db 
from app.models.book import Book

books_bp = Blueprint ("books", __name__, url_prefix="/books")


def validate_book(book_id):
    
    try:
        book_id = int(book_id)
    except:
        abort(make_response({"message":f"Book {book_id} invalid"},400))

    book = Book.query.get(book_id)

    if not book:
        abort(make_response({"message":f"Book {book_id} not found"}, 404))

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
        books_response.append({
            "id": book.id,
            "title": book.title,
            "description": book.description
        })
    
    return jsonify (books_response), 200
    #return make_response ("Im a teapot"), 418

@books_bp.route("", methods=["POST"])

def create_book():

    request_body = request.get_json()
    new_book = Book(title= request_body["title"],
                    description = request_body["description"])
    
    db.session.add(new_book)
    db.session.commit()

    return make_response (jsonify(f"Book {new_book.title} succesfully created"),201)


@books_bp.route("/<book_id>" , methods= ["GET"])

def handle_book (book_id):

    book = validate_book(book_id)

    #Think this is from past waves

    if book == None:
        return make_response("", status=404)
    else:
        return {
            "id": book.id,
            "title": book.title,
            "description": book.description
        }

@books_bp.route("/<book_id>" , methods= ["PUT"])

def update_book(book_id):

    book = validate_book(book_id)

    request_body = request.get_json()

    book.title = request_body["title"]
    book.description = request_body["description"]

    db.session.commit()

    return make_response (jsonify(f"Book #{book.id} successfully updated",201))

@books_bp.route("/<book_id>", methods = ["DELETE"])
def delete_book(book_id):
    book= validate_book(book_id)

    db.session.delete(book)
    db.session.commit()

    return make_response(jsonify(f"Book #{book.id} succesfully deleted",200))


    