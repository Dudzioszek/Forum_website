from flask import Flask, render_template, request, redirect, url_for, flash, session, g
import sqlite3
import os
from db_init import init_db

app = Flask(__name__)
app.secret_key = os.urandom(24)

DATABASE = 'debate_forum.db'



def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        db = get_db()
        g.user = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()

@app.route('/')
def index():
    # Retrieve topics from the database and pass them to the template
    db = get_db()
    topics = db.execute('SELECT * FROM topics ORDER BY timestamp DESC').fetchall()
    return render_template('index.html', topics=topics)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        email = request.form['email']

        # Check if the username already exists
        db = get_db()
        existing_user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        if existing_user:
            flash('Username already exists, please choose another one.', 'error')
        else:
            # Save the user to the database
            db.execute('INSERT INTO users (username, password, name, email) VALUES (?, ?, ?, ?)',
                       (username, password, name, email))
            db.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

        if user and password == user['password']:
            session['user_id'] = user['id']
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'error')

    return render_template('login.html')



@app.route('/create_topic', methods=['GET', 'POST'])
def create_topic():
    if request.method == 'POST':
        title = request.form['title']
        user_id = session.get('user_id')

        if not user_id:
            flash('You must be logged in to create a topic.', 'error')
            return redirect(url_for('login'))

        db = get_db()
        db.execute('INSERT INTO topics (title, user_id) VALUES (?, ?)', (title, user_id))
        db.commit()

        flash('Topic created successfully.', 'success')
        return redirect(url_for('index'))

    return render_template('create_topic.html')


@app.route('/topic/<int:topic_id>')
def topic(topic_id):
    db = get_db()

    # Fetch topic information
    topic = db.execute('SELECT * FROM topics WHERE id = ?', (topic_id,)).fetchone()

    # Fetch claims with user information
    claims = db.execute('''
        SELECT claims.id, claims.header, claims.user_id, users.username, 
            strftime('%Y-%m-%d %H:%M', claims.timestamp) AS formatted_timestamp
        FROM claims
        JOIN users ON users.id = claims.user_id
        WHERE claims.topic_id = ?
    ''', (topic_id,)).fetchall()

    # Fetch replies with user information
    replies = {}
    for claim in claims:
        replies[claim['id']] = db.execute('''
            SELECT replies.content, replies.user_id, users.username,
                strftime('%Y-%m-%d %H:%M', replies.timestamp) AS formatted_timestamp
            FROM replies
            JOIN users ON users.id = replies.user_id
            WHERE replies.claim_id = ?
        ''', (claim['id'],)).fetchall()



    return render_template('topic.html', topic=topic, claims=claims, replies=replies)






@app.route('/topic/<int:topic_id>/add_claim', methods=['POST'])
def add_claim(topic_id):
    header = request.form['header']
    user_id = session['user_id']
    db = get_db()
    db.execute('INSERT INTO claims (header, user_id, topic_id) VALUES (?, ?, ?)', (header, user_id, topic_id))
    db.commit()
    return redirect(url_for('topic', topic_id=topic_id))





@app.route('/claim/<int:claim_id>')
def claim_details(claim_id):
    db = get_db()
    claim = db.execute('SELECT * FROM claims WHERE id = ?', (claim_id,)).fetchone()
    replies = db.execute('SELECT * FROM replies WHERE claim_id = ? ORDER BY timestamp DESC', (claim_id,)).fetchall()
    return render_template('claim_details.html', claim=claim, replies=replies)



@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have successfully logged out.', 'success')
    return redirect(url_for('index'))

@app.route('/api/topic/<int:topic_id>/claim/<int:claim_id>/add_reply', methods=('POST',))
def api_add_reply(topic_id, claim_id):
    content = request.form['content']
    user_id = session['user_id']
    db = get_db()
    db.execute('INSERT INTO replies (content, user_id, claim_id) VALUES (?, ?, ?)', (content, user_id, claim_id))
    db.commit()
    return {"status": "success"}






if __name__ == '__main__':
    init_db(app, get_db)
    app.run()


