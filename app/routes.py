# app/routes.py
from flask import request, jsonify, current_app
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from . import db
from .models import User, Book, Review, JournalEntry
from .auth import hash_password, verify_password, generate_token
from . import create_app
from .nyt_client import fetch_books_from_nyt

app = create_app()


def populate_books(list_name="hardcover-fiction"):
    # Fetch books from NYT API
    books = fetch_books_from_nyt(list_name)
    if not books:
        return jsonify({"error": "No books found"}), 404

    for book in books:
        new_book = Book(
            title=book["title"],
            author=book["author"],
            description=book.get("description", "No description available"),
            genre=book.get("primary_isbn13", ""),  # Could use ISBN for a unique genre field
            average_rating=0.0  # Set to 0, or update if you have a rating system
        )
        db.session.add(new_book)
    
    db.session.commit()
    return jsonify({"message": "Books added to the database"}), 200

book_bp = Blueprint("book_bp", __name__)

@book_bp.route("/populate_books", methods=["POST"])
def populate_books_route():
    return populate_books(list_name="hardcover-fiction")

@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    user = User(
        username=data["username"],
        email=data["email"],
        password_hash=hash_password(data["password"]),
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "User created successfully"}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(email=data["email"]).first()
    if not user or not verify_password(data["password"], user.password_hash):
        return jsonify({"msg": "Invalid credentials"}), 401

    token = generate_token(identity=user.id)
    return jsonify({"access_token": token}), 200

@app.route("/books", methods=["POST"])
@jwt_required()
def add_book():
    data = request.json
    book = Book(
        title=data["title"],
        author=data["author"],
        description=data.get("description"),
        genre=data.get("genre"),
    )
    db.session.add(book)
    db.session.commit()
    return jsonify({"msg": "Book added successfully"}), 201

@app.route("/books/<int:book_id>/review", methods=["POST"])
@jwt_required()
def add_review(book_id):
    user_id = get_jwt_identity()
    data = request.json
    review = Review(
        user_id=user_id,
        book_id=book_id,
        rating=data["rating"],
        review_text=data.get("review_text"),
    )
    db.session.add(review)
    db.session.commit()
    return jsonify({"msg": "Review added successfully"}), 201

@app.route("/books/<int:book_id>/journal", methods=["POST"])
@jwt_required()
def add_journal(book_id):
    user_id = get_jwt_identity()
    data = request.json
    journal = JournalEntry(
        user_id=user_id,
        book_id=book_id,
        entry_text=data["entry_text"],
    )
    db.session.add(journal)
    db.session.commit()
    return jsonify({"msg": "Journal entry added successfully"}), 201

