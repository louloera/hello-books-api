from app import db

class Author(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.String)
    books = db.relationship("Book", back_populates="author")

    def to_dict(self):
        author_as_dict={}
        author_as_dict["id"] = self.id
        author_as_dict["name"] = self.name
        book_names =[]
        for book in self.books:
            book_names.append(book.title)
            
        author_as_dict["books"] = book_names
        

        return author_as_dict
    
    @classmethod
    def from_dict(cls, author_data):
        new_author = Author(name=author_data["name"])
        return new_author
    


