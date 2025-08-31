import os
from flask import Blueprint, jsonify, abort, g
from contextlib import closing
from database import get_db
from auth import require_auth
from utils import store_path

delete_bp = Blueprint('delete', __name__)

@delete_bp.route('/delete/<string:file_hash>', methods=['DELETE'])
@require_auth 
def delete(file_hash: str):
    db = get_db()
    with closing(db.cursor()) as cur:
        cur.execute(
            "SELECT 1 FROM ownerships WHERE hash=? AND owner=?",
            (file_hash, g.current_user)
        )
        if cur.fetchone() is None:
            abort(404, description="File not found for this user or not owned by user")

        cur.execute(
            "DELETE FROM ownerships WHERE hash=? AND owner=?",
            (file_hash, g.current_user)
        )

        cur.execute("SELECT COUNT(*) as c FROM ownerships WHERE hash=?", (file_hash,))
        remaining = cur.fetchone()[0]

        if remaining == 0:
            cur.execute("DELETE FROM files WHERE hash=?", (file_hash,))
            path = store_path(file_hash)
            try:
                os.remove(path)
            except FileNotFoundError:
                pass

    return jsonify({
        "status": "deleted",
        "hash": file_hash,
        "owner": g.current_user
    }), 200
