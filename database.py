import os
import sqlite3
from flask import g
from contextlib import closing
from config import DB_PATH

SCHEMA = """
PRAGMA journal_mode=WAL;
CREATE TABLE IF NOT EXISTS files (
    hash TEXT PRIMARY KEY,
    size INTEGER NOT NULL,
    mime TEXT,
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS ownerships (
    hash TEXT NOT NULL,
    owner TEXT NOT NULL,
    original_name TEXT,
    uploaded_at TEXT NOT NULL,
    PRIMARY KEY (hash, owner),
    FOREIGN KEY (hash) REFERENCES files(hash) ON DELETE CASCADE
);
"""

def get_db():
    conn = getattr(g, '_db', None)
    if conn is None:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        conn = g._db = sqlite3.connect(DB_PATH, isolation_level=None, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        with closing(conn.cursor()) as cur:
            for stmt in SCHEMA.strip().split(';'):
                s = stmt.strip()
                if s:
                    cur.execute(s)
    return conn

def init_db():
    get_db()

def close_db(exception=None):
    conn = getattr(g, '_db', None)
    if conn is not None:
        conn.close()
        g._db = None
