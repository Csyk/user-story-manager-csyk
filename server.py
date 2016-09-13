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


@app.route('/story', methods=['GET'])
def add_story():
    """Add story"""
    return render_template('form.html', title='Add story')


@app.route('/story/submit', methods=['POST'])
def new_story():
    """Add story"""
    db = get_db()
    db.execute("""INSERT INTO entries (story_title, user_story, acceptance_criteria, business_value, estimation)
               VALUES (?, ?, ?, ?, ?)""", [request.form["story_title"], request.form["user_story"],
                                           request.form["acceptance_criteria"], request.form["business_value"],
                                           request.form["estimation"]])
    db.commit()
    return redirect(url_for('list_stories'))  # redirect to another route


@app.route('/')
@app.route('/list', methods=['GET'])  # default GET
def list_stories():
    """Show stories"""
    db = get_db()
    query = """SELECT * FROM entries"""
    cur = db.execute(query)
    stories = cur.fetchall()
    return render_template('list.html', entries=stories)


if __name__ == '__main__':
    app.run(debug=True)
