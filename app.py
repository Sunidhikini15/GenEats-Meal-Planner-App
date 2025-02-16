from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.config["SECRET_KEY"] = "1RVU23CSE106"

# Function to connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn

# Initialize the database and create the users table if it doesn't exist
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Home Route (Login Page)
@app.route('/')
def home():
    return render_template('home.html')

# Login Page Route (GET)
@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

# Signup Page (GET)
@app.route('/signup', methods=['GET'])
def signup_page():
    return render_template('signup.html')

# Signup Route (POST)
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json  # Expecting JSON request body
    username = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"message": "Missing required fields"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the user already exists
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    existing_user = cursor.fetchone()

    if existing_user:
        conn.close()
        return jsonify({"message": "User already exists!"}), 400

    # Hash the password before storing
    hashed_password = generate_password_hash(password)

    # Insert the new user into the database
    cursor.execute(
        "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
        (username, email, hashed_password)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Signup successful!"}), 201

# Login Route (POST)
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    if not email or not password:
        flash("Missing email or password", "error")
        return redirect(url_for('login_page'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch the user from the database
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()

    if user and check_password_hash(user['password'], password):
        session['user'] = user['email']  # Store user session
        return redirect(url_for('mainpage'))  # Redirect to main page after login

    flash("Invalid credentials", "error")
    return redirect(url_for('login_page'))  # Stay on login page if invalid credentials
    

# Logout Route
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

# Main Page Route (After Login)
@app.route('/mainpage')
def main_page():
    return render_template('mainpage.html')

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)