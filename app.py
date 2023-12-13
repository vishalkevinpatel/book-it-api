from flask import Flask, request
from flask_cors import CORS
from werkzeug.security import check_password_hash, generate_password_hash
import db
import bcrypt


app = Flask(__name__)
cors = CORS(app, origins=["http://localhost:5173", "*"])


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/books.json")
def index():
    return db.books_all()


@app.route("/books.json", methods=["POST"])
def create():
    title = request.form.get("title")
    author = request.form.get("author")
    description = request.form.get("description")
    image = request.form.get("image")
    return db.books_create(title, author, description, image)


@app.route("/books/<id>.json")
def show(id):
    return db.books_find_by_id(id)


@app.route("/books/<id>.json", methods=["PATCH"])
def update(id):
    book = db.books_find_by_id(id)
    title = request.form.get("title", book["title"])
    author = request.form.get("author", book["author"])
    description = request.form.get("description", book["description"])
    image = request.form.get("image", book["image"])
    return db.books_update_by_id(id, title, author, description, image)


@app.route("/books/<id>.json", methods=["DELETE"])
def destroy(id):
    return db.books_destroy_by_id(id)


@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')