import sqlite3
from flask import g

def init_db(app, get_db):
    with app.app_context():
        db = get_db()

        # Define table creation queries
        tables = {
            "users": '''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    name TEXT,
                    email TEXT
                );
            ''',
            "topics": '''
                CREATE TABLE IF NOT EXISTS topics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    user_id INTEGER NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                );
            ''',
            "claims": '''
                CREATE TABLE IF NOT EXISTS claims (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    header TEXT NOT NULL,
                    user_id INTEGER NOT NULL,
                    topic_id INTEGER NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id),
                    FOREIGN KEY (topic_id) REFERENCES topics (id)
                );
            ''',
            "replies": '''
                CREATE TABLE IF NOT EXISTS replies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    user_id INTEGER NOT NULL,
                    author_id INTEGER,
                    claim_id INTEGER NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id),
                    FOREIGN KEY (claim_id) REFERENCES claims (id),
                    FOREIGN KEY (author_id) REFERENCES users (id)
                );
            '''
        }

        # Execute each table creation query
        for table, query in tables.items():
            db.execute(query)

        db.commit()
