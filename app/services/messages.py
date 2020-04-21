import uuid
from datetime import datetime
from ..services import util, sqlite

def add(users_id, message_text):
    query = "INSERT INTO messages (created_at, users_id, message) VALUES (?,?,?)"
    params = (datetime.utcnow().isoformat(), users_id, message_text)
    if sqlite.write(query, params):
        return True
    return False

def get_all():
    query = "SELECT * FROM messages ORDER BY created_at DESC"
    return sqlite.read(query)
