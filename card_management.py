from flask import Blueprint, render_template, jsonify, session
from functools import wraps
import sqlite3
import traceback

card_management = Blueprint('card_management', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated_function

@card_management.route('/manage_cards')
@login_required
def manage_cards():
    return render_template('manage_cards.html')

@card_management.route('/api/cards/<int:card_id>', methods=['DELETE'])
@login_required
def delete_card(card_id):
    try:
        with sqlite3.connect('kanban.db') as conn:
            c = conn.cursor()
            c.execute("DELETE FROM kanban_cards WHERE id=? AND organization=?", (card_id, session['organization']))
            if c.rowcount == 0:
                return jsonify({"error": "Card not found or unauthorized"}), 404
        return jsonify({"message": "Card deleted successfully"}), 200
    except Exception as e:
        print(f"Error in delete_card: {str(e)}")
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500