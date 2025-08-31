from flask import Blueprint, request, abort, jsonify, g
from tempfile import NamedTemporaryFile
from datetime import datetime, timezone
from contextlib import closing
from database import get_db
from auth import require_auth
from utils import algo, store_path
import os

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload', methods=['POST'])
@require_auth
def upload():
    if 'file' not in request.files:
        abort(400, description="No file part 'file' in form-data")
    
    up = request.files['file']
    if up.filename == '':
        abort(400, description="Empty filename")

    hasher = algo()
    with NamedTemporaryFile(delete=False) as tmp:
        while True:
            chunk = up.stream.read(1024 * 1024)
            if not chunk:
                break
            hasher.update(chunk)
            tmp.write(chunk)
        tmp_path = tmp.name

    file_hash = hasher.hexdigest()
    dest_path = store_path(file_hash)

    if not os.path.exists(dest_path):
        os.replace(tmp_path, dest_path)
    else:
        os.remove(tmp_path)

    now = datetime.now(timezone.utc).isoformat()

    db = get_db()
    with closing(db.cursor()) as cur:
        cur.execute(
            "INSERT OR IGNORE INTO files(hash, size, mime, created_at) VALUES(?,?,?,?)",
            (file_hash, os.path.getsize(dest_path), up.mimetype, now)
        )
        cur.execute(
            "INSERT OR IGNORE INTO ownerships(hash, owner, original_name, uploaded_at) VALUES(?,?,?,?)",
            (file_hash, g.current_user, up.filename, now)
        )

    return jsonify({
        "hash": file_hash,
        "size": os.path.getsize(dest_path),
        "mime": up.mimetype,
        "owner": g.current_user
    }), 201
