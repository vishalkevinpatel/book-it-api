from flask import Flask, request
import db

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/books.json")
def index():
    return db.books_all()
