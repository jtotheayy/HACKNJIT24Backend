from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask!"

if __name__ == '__main__':
    app.run(debug=True)
    
    '''
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"error": "Missing fields"}), 400

    users[email] = {"username": username, "password": password}
    return jsonify({"message": "User created successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = users.get(email)
    if user and user['password'] == password:
        return jsonify({"message": "Login successful", "user": user}), 200
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/searchbooks', methods=['GET'])
def search_books():
    query = request.args.get('query')
    response = requests.get(f'https://api.nytimes.com/svc/books/v3/reviews.json?title={query}&api-key={NYT_API_KEY}')
    return jsonify(response.json()), response.status_code

@app.route('/add-to-read', methods=['POST'])
def add_to_read():
    data = request.get_json()
    email = data.get('email')  # Assuming email is used to identify the user
    book_id = data.get('book_id')
    
    if email not in user_books:
        user_books[email] = []
    user_books[email].append(book_id)
    
    return jsonify({"message": "Book added to your list"}), 201

@app.route('/get-books', methods=['GET'])
def get_books():
    email = request.args.get('email')
    books = user_books.get(email, [])
    return jsonify(books), 200

if __name__ == '__main__':
    app.run(debug=True)
    '''