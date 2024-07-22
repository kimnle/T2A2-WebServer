from init import db, ma
from marshmallow import fields
from marshmallow.validate import OneOf

VALID_RATINGS = (1, 2, 3, 4, 5)

class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)

    user = db.relationship("User", back_populates="reviews")
    book = db.relationship("Book", back_populates="reviews")

class ReviewSchema(ma.Schema):

    user = fields.Nested("UserSchema", only=["name"])
    book = fields.Nested("BookSchema", exclude=["reviews"])

    rating = fields.Integer(required=True, validate=OneOf(VALID_RATINGS, error="Must be between 1 to 5"))

    class Meta:
        fields = ("id", "rating", "comment", "user", "book")
        ordered = True

review_schema = ReviewSchema()

reviews_schema = ReviewSchema(many=True)