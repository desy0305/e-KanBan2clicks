import sqlite3
from flask_bcrypt import Bcrypt

# Initialize Flask-Bcrypt
bcrypt = Bcrypt()

def init_db():
    with sqlite3.connect('kanban.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      username TEXT UNIQUE NOT NULL,
                      password TEXT NOT NULL,
                      organization TEXT NOT NULL)''')
        c.execute('''CREATE TABLE IF NOT EXISTS kanban_cards
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      item TEXT NOT NULL,
                      quantity INTEGER NOT NULL,
                      status TEXT NOT NULL,
                      location TEXT NOT NULL,
                      supplier TEXT NOT NULL,
                      organization TEXT NOT NULL)''')
        conn.commit()

def add_test_user():
    init_db()  # Ensure tables are created
    with sqlite3.connect('kanban.db') as conn:
        c = conn.cursor()
        
        # Check if the user already exists
        c.execute("SELECT * FROM users WHERE username = ?", ("testuser",))
        if c.fetchone() is None:
            # Hash the password
            hashed_password = bcrypt.generate_password_hash("testpassword").decode('utf-8')
            
            # Insert the test user
            c.execute("INSERT INTO users (username, password, organization) VALUES (?, ?, ?)",
                      ("testuser", hashed_password, "TestOrg"))
            
            print("Test user added successfully.")
        else:
            print("Test user already exists.")

if __name__ == "__main__":
    add_test_user()