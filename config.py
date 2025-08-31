import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
STORE_DIR = os.environ.get("STORE_DIR", os.path.join(BASE_DIR, "store"))
DB_PATH = os.environ.get("DB_PATH", os.path.join(STORE_DIR, "meta.db"))
HASH_ALGO = os.environ.get("HASH_ALGO", "sha256").lower()
USERS_ENV = os.environ.get("USERS", "alice:password,bob:secret")