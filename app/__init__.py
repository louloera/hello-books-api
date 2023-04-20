from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__)

    from.routes import hello_world_pb
    app.register_blueprint(hello_world_pb)

    return app

def create_app():
    app= Flask(__name__)

    from .routes import books_bp
    app.register_blueprint(books_bp)

    return app
