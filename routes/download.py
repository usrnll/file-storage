import os
from flask import Blueprint, send_file, abort
from utils import store_path

download_bp = Blueprint('download', __name__)

@download_bp.route('/download/<string:file_hash>', methods=['GET'])
def download(file_hash: str):
    path = store_path(file_hash)
    
    if not os.path.exists(path):
        abort(404, description="File not found")

    return send_file(
        path,
        as_attachment=True,
        download_name=file_hash
    )
