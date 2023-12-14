from flask import Flask, request
from flask import flash
from flask_cors import CORS
from werkzeug.security import check_password_hash, generate_password_hash
import db


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


@app.route("/users.json", methods=["POST"])
def users_create():
    username = request.form.get("username")
    password = request.form.get("password")

    return db.user_create(username, generate_password_hash(password))
