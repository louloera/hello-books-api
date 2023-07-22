from app import db 

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    author = db.relationship("Author",back_populates="books")
    genres = db.relationship("Genre", secondary="book_genre", backref="books")

    def to_dict(self):
        book_as_dict={}
        book_as_dict["id"] = self.id
        book_as_dict["title"] = self.title
        book_as_dict["description"] = self.description
        if self.author:
            book_as_dict["author"] = self.author.name
        if self.genres:
            genre_names = [genre.name for genre in self.genres]
            book_as_dict["genres"] = genre_names

        return book_as_dict
    
    @classmethod
    def from_dict(cls, book_data, author_id = None):
        new_book = Book(title=book_data["title"], 
                        description = book_data["description"],
                        author_id = author_id)
        return new_book
    