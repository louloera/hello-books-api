import pytest
from app import create_app 
from app import db
from flask.signals import request_finished
from app.models.book import Book 


@pytest.fixture

def app():
    app = create_app({"TESTING": True})

    @request_finished.connect_via(app)

    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app 

    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture 
#it has app so we can know that the database is initialialized
def two_saved_books(app):
    #Arrange
    ocean_book = Book (title= "Ocean Book",
                    description = "watr 4evr")
    mountain_book = Book(title = "Moutain Book",
                    description= "i luv 2 climb rocks")
    db.session.add_all([ocean_book, mountain_book])
    db.session.commit()


    

