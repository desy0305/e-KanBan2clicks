from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_bcrypt import Bcrypt
from functools import wraps
import sqlite3
import os
import traceback
from card_management import card_management

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Set a secret key for session management
bcrypt = Bcrypt(app)
app.register_blueprint(card_management)

# Database initialization
def init_db():
    with sqlite3.connect('kanban.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      username TEXT UNIQUE NOT NULL,
                      password TEXT NOT NULL,
                      organization TEXT NOT NULL)''')
        
        # Check if the organization column exists in kanban_cards table
        c.execute("PRAGMA table_info(kanban_cards)")
        columns = [column[1] for column in c.fetchall()]
        
        if 'organization' not in columns:
            # Add organization column to existing table
            c.execute('''ALTER TABLE kanban_cards ADD COLUMN organization TEXT''')
        else:
            # Create the table with the organization column
            c.execute('''CREATE TABLE IF NOT EXISTS kanban_cards
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          item TEXT NOT NULL,
                          quantity INTEGER NOT NULL,
                          status TEXT NOT NULL,
                          location TEXT NOT NULL,
                          supplier TEXT NOT NULL,
                          organization TEXT)''')
        
        conn.commit()

# Initialize database
init_db()

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        organization = request.form['organization']
        
        with sqlite3.connect('kanban.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE username = ?", (username,))
            if c.fetchone() is not None:
                flash('Username already exists. Please choose a different one.', 'error')
            else:
                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                c.execute("INSERT INTO users (username, password, organization) VALUES (?, ?, ?)",
                          (username, hashed_password, organization))
                conn.commit()
                flash('Registration successful. Please log in.', 'success')
                return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect('kanban.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = c.fetchone()
            if user and bcrypt.check_password_hash(user[2], password):
                session['user_id'] = user[0]
                session['username'] = user[1]
                session['organization'] = user[3]
                return redirect(url_for('index'))
            else:
                flash('Invalid username or password', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('organization', None)
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return render_template('index.html', manage_cards_url=url_for('card_management.manage_cards'))

@app.route('/api/user')
@login_required
def get_user():
    return jsonify({"username": session.get('username'), "organization": session.get('organization')})

@app.route('/api/cards', methods=['GET'])
@login_required
def get_cards():
    try:
        with sqlite3.connect('kanban.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM kanban_cards WHERE organization = ?", (session['organization'],))
            cards = [dict(id=row[0], item=row[1], quantity=row[2], status=row[3], location=row[4], supplier=row[5]) for row in c.fetchall()]
        return jsonify(cards)
    except Exception as e:
        app.logger.error(f"Error in get_cards: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

@app.route('/api/cards', methods=['POST'])
@login_required
def add_card():
    try:
        card = request.json
        if not all(key in card for key in ['item', 'quantity', 'status', 'location', 'supplier']):
            return jsonify({"error": "Missing required fields"}), 400
        
        quantity = card.get('quantity')
        if quantity is None or not isinstance(quantity, (int, float)):
            return jsonify({"error": "Invalid quantity value"}), 400

        with sqlite3.connect('kanban.db') as conn:
            c = conn.cursor()
            c.execute("INSERT INTO kanban_cards (item, quantity, status, location, supplier, organization) VALUES (?, ?, ?, ?, ?, ?)",
                      (card['item'], int(quantity), card['status'], card['location'], card['supplier'], session['organization']))
            conn.commit()
            card_id = c.lastrowid
        return jsonify({"id": card_id, **card}), 201
    except Exception as e:
        app.logger.error(f"Error in add_card: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 400

@app.route('/api/cards/<int:card_id>', methods=['PUT'])
@login_required
def update_card(card_id):
    try:
        card = request.json
        with sqlite3.connect('kanban.db') as conn:
            c = conn.cursor()
            c.execute("UPDATE kanban_cards SET status=? WHERE id=? AND organization=?", (card['status'], card_id, session['organization']))
            if c.rowcount == 0:
                return jsonify({"error": "Card not found or unauthorized"}), 404
        return jsonify({"message": "Card updated successfully"}), 200
    except Exception as e:
        app.logger.error(f"Error in update_card: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

@app.route('/api/items', methods=['GET'])
@login_required
def get_items():
    try:
        with sqlite3.connect('kanban.db') as conn:
            c = conn.cursor()
            c.execute("SELECT DISTINCT item FROM kanban_cards WHERE organization = ?", (session['organization'],))
            items = [row[0] for row in c.fetchall()]
        return jsonify(items)
    except Exception as e:
        app.logger.error(f"Error in get_items: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)