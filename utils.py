import os
import hashlib
from config import STORE_DIR, HASH_ALGO

def algo():
    if HASH_ALGO == 'sha256':
        return hashlib.sha256()
    if HASH_ALGO == 'blake2b':
        return hashlib.blake2b()
    if HASH_ALGO == 'sha1':
        return hashlib.sha1()
    raise ValueError(f"Unsupported HASH_ALGO: {HASH_ALGO}")

def store_path(file_hash: str) -> str:
    subdir = file_hash[:2]
    dir_path = os.path.join(STORE_DIR, subdir)
    os.makedirs(dir_path, exist_ok=True)
    return os.path.join(dir_path, file_hash)