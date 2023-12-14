import sqlite3


def connect_to_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


def initial_setup():
    conn = connect_to_db()
    conn.execute(
        """
        DROP TABLE IF EXISTS books;
        """
    )
    conn.execute(
        """
        DROP TABLE IF EXISTS users;
        """
    )
    conn.execute(
        """
        DROP TABLE IF EXISTS collections;
        """
    )

    conn.execute(
        """
        CREATE TABLE books (
          id INTEGER PRIMARY KEY NOT NULL,
          title TEXT NOT NULL,
          author TEXT NOT NULL,
          description TEXT,
          image TEXT
        );
        """
    )
    conn.execute(
        """
        CREATE TABLE users (
          id INTEGER PRIMARY KEY NOT NULL,
          username TEXT NOT NULL UNIQUE,
          hashed_password TEXT NOT NULL
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE collections (
          id INTEGER PRIMARY KEY NOT NULL,
          user_id INTEGER NOT NULL,
          book_id INTEGER NOT NULL,
          FOREIGN KEY (user_id) REFERENCES users(id),
          FOREIGN KEY (book_id) REFERENCES books(id)
        )
        """
    )
    conn.commit()
    print("Table created successfully")

    books_seed_data = [
        (
            "Harry Potter and the Chamber of Secrets",
            "JK Rowling",
            "book 2",
            "https://upload.wikimedia.org/wikipedia/en/5/5c/Harry_Potter_and_the_Chamber_of_Secrets.jpg",
        ),
        (
            "Harry Potter and the Goblet of Fire",
            "JK Rowling",
            "book 4",
            "https://upload.wikimedia.org/wikipedia/en/b/b6/Harry_Potter_and_the_Goblet_of_Fire_cover.png",
        ),
        (
            "Harry Potter and the Order of the Phoenix",
            "JK Rowling",
            "book 5",
            "https://upload.wikimedia.org/wikipedia/en/thumb/7/70/Harry_Potter_and_the_Order_of_the_Phoenix.jpg/220px-Harry_Potter_and_the_Order_of_the_Phoenix.jpg",
        ),
    ]
    conn.executemany(
        """
        INSERT INTO books (title, author, description, image)
        VALUES (?,?,?,?)
        """,
        books_seed_data,
    )
    conn.commit()
    print("Seed data created successfully with books")

    conn.close()


if __name__ == "__main__":
    initial_setup()


def books_all():
    conn = connect_to_db()
    rows = conn.execute(
        """
        SELECT * FROM books
        """
    ).fetchall()
    return [dict(row) for row in rows]


def books_create(title, author, description, image):
    conn = connect_to_db()
    row = conn.execute(
        """
        INSERT INTO books (title, author,description,image)
        VALUES (?, ?, ?,?)
        RETURNING *
        """,
        (title, author, description, image),
    ).fetchone()
    conn.commit()
    return dict(row)


def books_find_by_id(id):
    conn = connect_to_db()
    row = conn.execute(
        """
        SELECT * FROM books
        WHERE id = ?
        """,
        id,
    ).fetchone()
    return dict(row)


def books_update_by_id(id, title, author, description, image):
    conn = connect_to_db()
    row = conn.execute(
        """
        UPDATE books SET title = ?, author = ?, description = ?, image = ?
        WHERE id = ?
        RETURNING *
        """,
        (title, author, description, image, id),
    ).fetchone()
    conn.commit()
    return dict(row)


def books_destroy_by_id(id):
    conn = connect_to_db()
    row = conn.execute(
        """
        DELETE from books
        WHERE id = ?
        """,
        id,
    )
    conn.commit()
    return {"message": "Book destroyed successfully"}


def user_create(username, hashed_password):
    conn = connect_to_db()
    row = conn.execute(
        """
        INSERT INTO users (username, hashed_password)
        VALUES (?, ?)
        RETURNING *
        """,
        (username, hashed_password),
    ).fetchone()
    conn.commit()
    return dict(row)
