from flask import Flask, jsonify
from config import HASH_ALGO
from routes.upload import upload_bp
from routes.download import download_bp
from routes.delete import delete_bp
from database import init_db, close_db

app = Flask(__name__)

app.register_blueprint(upload_bp)
app.register_blueprint(download_bp)
app.register_blueprint(delete_bp)

@app.before_request
def before_request():
    init_db()

@app.teardown_appcontext
def teardown_db(exception):
    close_db(exception)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "algo": HASH_ALGO}), 200

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', '8000'))
    app.run(host='0.0.0.0', port=port)