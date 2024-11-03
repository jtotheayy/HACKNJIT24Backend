from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from . import db
from .models import User, Book, Review, JournalEntry
from .auth import hash_password, verify_password, generate_token
from .nyt_client import fetch_books_from_nyt
from .nyt_client import fetch_all_list_names

book_bp = Blueprint("book_bp", __name__)


@book_bp.route("/populate_books", methods=["POST"])
def populate_books_route():
    # Step 1: Fetch all list names
    list_names = fetch_all_list_names()  # Corrected function call
    if not list_names:
        return jsonify({"error": "Failed to retrieve list names"}), 500

    total_books_added = 0
    for list_name in list_names:
        # Step 2: Fetch books for each list
        books = fetch_books_from_nyt(list_name)
        if not books:
            continue

        for book_data in books:
            # Step 3: Check for duplicates based on ISBN
            isbn = book_data.get("primary_isbn13")  # Use primary_isbn13 as unique identifier
            if isbn and Book.query.filter_by(genre=isbn).first():
                continue  # Skip if book already exists

            # Step 4: Add new book to the database
            new_book = Book(
                title=book_data["title"],
                author=book_data["author"],
                description=book_data.get("description", "No description available"),
                genre=isbn,  # Using ISBN as a unique genre/category
                average_rating=0.0
            )
            db.session.add(new_book)
            total_books_added += 1

    db.session.commit()
    return jsonify({"message": f"{total_books_added} books added to the database"}), 200
    

@book_bp.route("/signup", methods=["POST"])
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

@book_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(email=data["email"]).first()
    if not user or not verify_password(data["password"], user.password_hash):
        return jsonify({"msg": "Invalid credentials"}), 401

    token = generate_token(identity=user.id)
    return jsonify({"access_token": token}), 200

@book_bp.route("/books", methods=["POST"])
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

@book_bp.route("/books/<int:book_id>/review", methods=["POST"])
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

@book_bp.route("/books/<int:book_id>/journal", methods=["POST"])
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

