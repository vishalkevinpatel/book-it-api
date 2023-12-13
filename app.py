from flask import Flask, request
import db

app = Flask(__name__)


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
