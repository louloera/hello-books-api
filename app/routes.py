from flask import Blueprint, jsonify, abort, make_response


hello_world_pb = Blueprint("hello_world", __name__)

@hello_world_pb.route("/hello-world", methods=["GET"])

def say_hello_world():
    my_beautiful_world = "Hello World!"
    return my_beautiful_world, 200

@hello_world_pb.route("/hello/JSON", methods=["GET"])

def say_hello_json():
    return {
        "name": "Lou",
        "message": "Ando Programando",
        "hobbies": ["programar", "cotorrear"]
    }, 200

@hello_world_pb.route("/broken-endpoint-with-broken-server-code")

def broken_endpoint():
    response_body= {
        "name": "Lou",
        "message": "Ando Programando",
        "hobbies": ["programar", "cotorrear"]

    }

    new_hobby = "Boxing"
    response_body["hobbies"].append(new_hobby)
    return response_body


class Book:
    def __init__(self, id, title, description):
        self.id = id 
        self.title = title 
        self.description = description 

books = [
    Book(1, "Fictional Book Title 1", "A fantasy novel set in an imaginary world."),
    Book(2, "Fictional Book Title 2", "A fantasy novel set in an imaginary world."),
    Book(3, "Fictional Book Title 2", "A fantasy novel set in an imaginary world.")
]

def validate_book(book_id):
    try:
        book_id = int(book_id)
    except:
        abort(make_response({"message":f"Book {book_id} invalid"},400))
    for book in books:
        if book.id == book_id:
            return book
    abort(make_response({"message":f"Book {book_id} not found"}, 404))

books_bp = Blueprint ("books", __name__, url_prefix="/books")

@books_bp.route("", methods=["GET"])
def handle_books():
    books_response = []
    for book in books:
        books_response.append({
            "id": book.id,
            "title": book.title,
            "description": book.description
        })
    return jsonify (books_response)

@books_bp.route("/<book_id>" , methods= ["GET"])

def handle_book (book_id):
    book = validate_book(book_id)

    return {
            "id": book.id,
            "title": book.title,
            "description": book.description
    }
    # try:
    #     book_id = int(book_id)
    # except:
    #     return {"message":f"Book {book_id} invalid"},400
    
    # for book in books:
    #     if book_id == book.id:
    #         return {
    #         "id": book.id,
    #         "title": book.title,
    #         "description": book.description
    #     }
    # return {"message":f"Book {book_id} not found"}, 404

    #NOMAS POR NOMAS
    