from init import db, ma
from marshmallow import fields

class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    genre = db.Column(db.String, nullable=False)
    summary = db.Column(db.String, nullable=False)

    club_books = db.relationship("ClubBook", back_populates="book", cascade="all, delete")
    reviews = db.relationship("Review", back_populates="book", cascade="all, delete")

class BookSchema(ma.Schema):

    club_books = fields.List(fields.Nested("ClubBookSchema", exclude=["book"]))
    reviews = fields.List(fields.Nested("ReviewSchema", exclude=["book"]))

    class Meta:
        fields = ("id", "title", "author", "genre", "summary", "club_books", "reviews")
        ordered = True

book_schema = BookSchema()

books_schema = BookSchema(many=True)