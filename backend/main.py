"""
This module provides a Flask application for user authentication and quote management.
It allows users to log in, manage their quotes, and view quotes from other users.
"""

import csv
import os
import random
import secrets

from dotenv import load_dotenv
from flask import redirect, url_for, Flask, request, jsonify, session
from flask_oauthlib.client import OAuth
from flask_cors import CORS
from langchain.llms import OpenAI

from db_interface import load_user_data, load_quotes_for_email, save_quote_to_csv, load_all_quotes

# Load environment variables from the .env file
load_dotenv()


"""
Self Note: Token JWT is different then Key JWT. 
This Key is generated one time in the begging of the server
"""


# Generation of a secret key for JWT
key = secrets.token_hex(32)
os.environ['JWT_SECRET_KEY'] = key
print("Generated JWT_SECRET_KEY: ", key)

from backend.routes.google_oauth import oauth_bp
from backend.routes.pages import pages_handlers_bp

# Configuration for environment variables
FILEPATH_DB_TABLE_ID_QUOTE_AUTHOR = os.environ['FILEPATH_DB_TABLE_ID_QUOTE_AUTHOR']
GOOGLE_CLIENT_ID = os.environ['GOOGLE_CLIENT_ID']

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
CORS(app, supports_credentials=True)
oauth = OAuth(app)

# Google OAuth configuration
google = oauth.remote_app(
    'google',
    consumer_key=GOOGLE_CLIENT_ID,
    consumer_secret=os.environ['YOUR_CLIENT_SECRET'],
    request_token_params={'scope': 'email profile'},
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)


@app.route('/')
def index():
    """Return a welcome message."""
    return jsonify({'message': 'Hello, from the Backend!'})


@app.route('/login', methods=['POST'])
def login():
    """Authenticate the user and start a session."""
    # Load user data
    users = load_user_data()
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Check if user exists and password matches
    if email in users and users[email] == password:
        session['email'] = email
        return jsonify(success=True, message="Login successful")
    else:
        return jsonify(success=False, message="Unauthorized"), 401


@app.route('/logout')
def logout():
    """End the user's session and redirect to the logout screen."""
    session.pop('email', None)
    return redirect(url_for('page_logout'))


@app.route('/get_logged_in_email', methods=['GET'])
def get_logged_in_email():
    """Return the email of the currently logged-in user."""
    email = session.get('email')
    if email:
        return jsonify(email=email)
    else:
        return jsonify({"error": "User not logged in"}), 403


@app.route('/generate_quote', methods=['GET'])
def generate_quote():
    llm = OpenAI()
    our_query = """
    You are a Guru of Inspirational Quotes for life, that touch the heart of people. 
    Give me one quote. No additional text before or after it. 
    Do not provide the author. It should be 100% from your creativity.
    Examples:
    The way to get started is to quit talking and begin doing.
    The future belongs to those who believe in the beauty of their dreams.
    Develop success from failures. Discouragement and failure are two of the surest stepping stones to success.
    Life is not worth living - unless it is lived for someone else.
    """

    completion = llm(our_query)
    return str(completion)


@app.route('/save_quote', methods=['POST'])
def save_quote():
    if 'email' in session:
        data = request.json
        quote = data.get('quote')
        author = data.get('author')
        if not author:
            author = session['email']
        saved_id = save_quote_to_csv(author, quote)
        if saved_id:
            return jsonify(success=True)
        else:
            return jsonify(success=False, message="Error saving the quote."), 500
    else:
        return jsonify(success=False, message="User not page_homepage in."), 403


@app.route('/save_quote_homepage', methods=['POST'])
def save_quote_homepage():
    data = request.json
    quote = data.get('quote')
    author = data.get('author')

    save_quote_to_csv(author, quote)


@app.route('/get_email_quotes')
def get_email_quotes():
    email = session.get('email')
    if not email:
        return jsonify(success=False, message="User not page_homepage in"), 403
    quotes = load_quotes_for_email(email)
    return jsonify(quotes=quotes)


@app.route('/edit_quote', methods=['POST'])
def edit_quote():
    old_quote = request.json.get('old_quote')
    new_quote = request.json.get('new_quote')
    email_of_user = session.get('email')  # Get the email of the page_homepage-in user

    if not old_quote or not new_quote:
        return jsonify({"success": False, "message": "Both old and new quotes are required."}), 400

    rows = []
    found = False
    with open(FILEPATH_DB_TABLE_ID_QUOTE_AUTHOR, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            # Assuming the quote is the fourth column and email is the second column
            if row[4] == old_quote and row[1] == email_of_user:
                found = True
                row[4] = new_quote  # Update the quote in this row
            rows.append(row)

    if not found:
        return jsonify({"success": False, "message": "Old quote not found."}), 404

    with open(FILEPATH_DB_TABLE_ID_QUOTE_AUTHOR, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    return jsonify({"success": True, "message": "Quote edited successfully."})


@app.route('/delete_quote', methods=['POST'])
def delete_quote():
    quote_to_delete = request.json.get('quote')
    email_of_user = session.get('email')  # Get the email of the page_homepage-in user

    if not quote_to_delete:
        return jsonify({"success": False, "message": "Quote is required."}), 400

    rows = []
    found = False
    with open(FILEPATH_DB_TABLE_ID_QUOTE_AUTHOR, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            # Assuming the quote is the fifth column and email is the second column
            if row[4] == quote_to_delete and row[1] == email_of_user:
                found = True
                continue  # Skip appending this row to the rows list
            rows.append(row)

    if not found:
        return jsonify({"success": False, "message": "Quote not found."}), 404

    with open(FILEPATH_DB_TABLE_ID_QUOTE_AUTHOR, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    return jsonify({"success": True, "message": "Quote deleted successfully."})


@app.route('/get_all_quotes')
def get_all_quotes():
    quotes = load_all_quotes()
    return jsonify(quotes=quotes)


@app.route('/get_random_quote', methods=['GET'])
def get_random_quote():
    try:
        quotes = []
        with open('../db/table_id_quote_author.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['author_is_user'] == 'False':
                    quotes.append({"quote": row['quote'], "author": row['author']})

        if not quotes:
            return jsonify({"error": "No quotes found where author_is_user is False"}), 404

        random_quote = random.choice(quotes)
        return jsonify(random_quote)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Register the blueprints
app.register_blueprint(oauth_bp, url_prefix='/oauth')
app.register_blueprint(pages_handlers_bp, url_prefix='/pages')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
