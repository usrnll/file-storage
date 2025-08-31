from functools import wraps
from flask import request, jsonify, g
import hmac
from config import USERS_ENV

USERS = dict(pair.split(":", 1) for pair in USERS_ENV.split(",") if ":" in pair)

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth:
            return jsonify({"error": "Authentication required"}), 401

        username = auth.username
        password = auth.password

        stored_password = USERS.get(username)
        if not stored_password or not hmac.compare_digest(stored_password, password):
            return jsonify({"error": "Invalid credentials"}), 403

        g.current_user = username
        return f(*args, **kwargs)

    return decorated
