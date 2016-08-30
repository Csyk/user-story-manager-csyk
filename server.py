from flask import Flask, g, request, redirect, url_for, render_template
import sqlite3

app = Flask(__name__)
DATABASE = 'database.db'


# DB connect
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def setup_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    print('Initialized the database.')


@app.route('/story', methods=['GET'])
def add_story():
    """Add story"""
    return render_template('form.html', title='Add story')


@app.route('/story', methods=['POST'])
def new_story():
    """Add story"""
    db = get_db()
    db.execute("""INSERT INTO app (Story title, User story, Acceptance Criteria, Business value, Estimation)
               VALUES (?, ?, ?, ?, ?)""",
               [request.form['Story title'], request.form['User story'], request.form['Acceptance Criteria'],
                request.form['Business value'], request.form['Estimation']])
    db.commit()
    return redirect(url_for('list_stories'))


@app.route('/list', methods=['GET'])
def list_stories():
    """Show stories"""
    db = get_db()
    query = """SELECT * FROM app"""
    cur = db.execute(query)
    stories = cur.fetchall()
    return render_template('list.html', entries=stories)


if __name__ == '__main__':
    app.run(debug=True)