import sqlite3


def create_tables(cursor):
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            username TEXT UNIQUE,
            hashed_password TEXT,
            email TEXT UNIQUE,
            state TEXT DEFAULT 'active'
        );
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Movies (
            movie_id INTEGER PRIMARY KEY AUTOINCREMENT,
            movie_name TEXT, 
            release_year INTEGER, 
            age_rating TEXT,
            runtime INTEGER,
            combined_rating REAL DEFAULT 0
        );
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Directors (
            director_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT
        );
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Movie_Directors (
            movie_id INTEGER,
            director_id INTEGER,
            PRIMARY KEY (movie_id, director_id),
            FOREIGN KEY (movie_id) REFERENCES Movies(movie_id) ON DELETE CASCADE,
            FOREIGN KEY (director_id) REFERENCES Directors(director_id) ON DELETE CASCADE
        );
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Writers (
            writer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT
        );
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Movie_Writers (
            movie_id INTEGER,
            writer_id INTEGER,
            PRIMARY KEY (movie_id, writer_id),
            FOREIGN KEY(movie_id) REFERENCES Movies(movie_id) ON DELETE CASCADE,
            FOREIGN KEY(writer_id) REFERENCES Writers(writer_id) ON DELETE CASCADE
        );
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Cast (
            actor_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT
        );
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Movie_Cast (
            movie_id INTEGER,
            actor_id INTEGER,
            PRIMARY KEY (movie_id, actor_id),
            FOREIGN KEY (movie_id) REFERENCES Movies(movie_id) ON DELETE CASCADE,
            FOREIGN KEY (actor_id) REFERENCES Cast(actor_id) ON DELETE CASCADE
        );
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Genres (
            genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
            genre_name TEXT UNIQUE
        );
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Movie_Genres (
            movie_id INTEGER,
            genre_id INTEGER,
            PRIMARY KEY (movie_id, genre_id),
            FOREIGN KEY(movie_id) REFERENCES Movies(movie_id) ON DELETE CASCADE,
            FOREIGN KEY(genre_id) REFERENCES Genres(genre_id) ON DELETE CASCADE
        );
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Comments (
            comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            movie_id INTEGER, 
            user_id INTEGER, 
            comment_text TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            parent_comment_id INTEGER,
            FOREIGN KEY(movie_id) REFERENCES Movies(movie_id) ON DELETE CASCADE,
            FOREIGN KEY(user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
            FOREIGN KEY(parent_comment_id) REFERENCES Comments(comment_id)
        );
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Ratings (
            rating_id INTEGER PRIMARY KEY AUTOINCREMENT,
            movie_id INTEGER,
            user_id INTEGER,
            rating_value REAL,
            review_text TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(movie_id) REFERENCES Movies(movie_id) ON DELETE CASCADE,
            FOREIGN KEY(user_id) REFERENCES Users(user_id) ON DELETE CASCADE
        );
    """
    )


if __name__ == "__main__":
    conn = sqlite3.connect("popcorn.db")
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    create_tables(cursor)
    conn.commit()

    cursor.execute("""
        SELECT name FROM sqlite_master WHERE type='table';
    """)
    
    tables = cursor.fetchall()

    print(f"Tables in the database: {tables}")

    conn.close()
