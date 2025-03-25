"""
So what do I need in my database.

Login / Sign-Up system:
    user_id, first_name, last_name, username, password (that must be hashed), email, state (like are they banned or not)

Movie Stuff:
    movie_id, movie_name, release_year, age_rating, runtime (best probs in minutes), rating, director/s, writer/s, cast, genre/s


No why am I struggling to make this database.

1) Values like director/s, writer/s, genre/s can have multiple values, so we can't store them in the same table
2) Since I can't store them in the same table, how do I go about seperating the tables.
3) Once seperating the tables, how can I connect all the tables - what must be a primary key, foreign key, do I need composite keys?
   (The hardest part in my mind atm)

How Do I go about fixing these problems?

So the main issue with having multiple director/s, writer/s, cast and genre/s under one movie table is that a many-to-many relationship is created
between the movie and the respective fields.

From school, I remember that my teacher said, you can add a junction table inbetween to get rid off this many-to-many relationship so that we have a
many-to-one relationship, then a one-to-many relationship which is valid.

[Tables Needed]
So for director/s: Directors, Movie_Directors, Movie
So for writer/s: Writers, Movie_Writers, Movie
So for cast: Cast, Movie_Cast, Movie
So for genre/s: Genres, Movie_Genres, Movie

Finally, what are all the tables we have, what would be their primary, foreign and composite keys (if any) ?

[ALL TABLES]
User, Movies, Directors, Movie_Directors, Writers, Movie_Writers, Cast, Movie_Cast, Genres, Movie_Genres, Comments, Ratings

[KEYS NEEDED FOR EACH]

[MAIN TABLES]
User : Primary Key = {user_id}
Movies: Primary Key = {movie_id}
Directors: Primary Key = {director_id}
Writers: Primary Key = {writer_id}
Cast: Primary Key = {actor_id}
Genres: Primary Key = {genre_id}

Comments: Primary Key = {comment_id}, Foreign Keys = {movie_id, user_id, parent_comment_id}
    - parent_comment_id is a "self-referential foreign key" that allows comments to reference other 
      comments (this should allow me to create the Reddit-like forum threads)
    
    - the foreign keys here ensure that each comment is associated with a valid movie and user.

Ratings: Primary Key = {rating_id}, Foreign Keys = {movie_id, user_id}
    - the foreign keys here used to ensure ratings are made on a valid movie with a valid user

[JUNCTION TABLES]
Movie_Directors : Composite Key = {movie_id, director_id}, Foreign Keys = {movie_id, director_id}
Movie_Writers : Composite Key = {movie_id, writer_id}, Foreign Keys = {movie_id, writer_id}
Movie_Cast : Composite Key = {movie_id, actor_id}, Foreign Keys = {movie_id, actor_id}
Movie_Genres : Composite Key = {movie_id, genre_id}, Foreign Keys = {movie_id, actor_id}

    - We use a composite key for all of these junction tables because 
      it allows us to display the unique many-to-many relationship
      these fields have with movies. For example, since Christopher Nolan 
      has only made one movie called "The Dark Knight", 
      the composite key maps him to the corresponding movie 
      (hence representing the unique relationship)

"""

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


def insert_data(cursor):
    cursor.execute(
        """
        INSERT INTO Movies (movie_name, release_year, age_rating, runtime, combined_rating)
        VALUES (?, ?, ?, ?, ?)
    """,
        ("The Dark Knight", 2008, "PG-13", 152, 9.0),
    )
    movie_id = cursor.lastrowid

    cursor.execute(
        """
        INSERT INTO Directors (first_name, last_name)
        VALUES (?, ?)
    """,
        ("Christopher", "Nolan"),
    )
    director_id = cursor.lastrowid

    cursor.execute(
        """
        INSERT INTO Movie_Directors (movie_id, director_id)
        VALUES(?, ?)
    """,
        (movie_id, director_id),
    )

    cursor.execute(
        """
        INSERT INTO Writers (first_name, last_name)
        VALUES (?, ?)
    """,
        ("Christopher", "Nolan"),
    )
    writer1_id = cursor.lastrowid

    cursor.execute(
        """
        INSERT INTO Writers (first_name, last_name)
        VALUES (?, ?)
    """,
        ("David S.", "Goyer"),
    )
    writer2_id = cursor.lastrowid

    cursor.execute(
        """
        INSERT INTO Writers (first_name, last_name)
        VALUES (?, ?)
    """,
        ("Jonathan", "Nolan"),
    )
    writer3_id = cursor.lastrowid

    cursor.execute(
        """
        INSERT INTO Movie_Writers (movie_id, writer_id)
        VALUES (?, ?)
    """,
        (movie_id, writer1_id),
    )

    cursor.execute(
        """
        INSERT INTO Movie_Writers (movie_id, writer_id)
        VALUES (?, ?)
    """,
        (movie_id, writer2_id),
    )

    cursor.execute(
        """
        INSERT INTO Movie_Writers (movie_id, writer_id)
        VALUES (?, ?)
    """,
        (movie_id, writer3_id),
    )

    cursor.execute(
        """
        INSERT INTO Cast (first_name, last_name)
        VALUES (?, ?)
    """,
        ("Christian", "Bale"),
    )
    actor1_id = cursor.lastrowid

    cursor.execute(
        """
        INSERT INTO Cast (first_name, last_name)
        VALUES (?, ?)
    """,
        ("Heath", "Ledger"),
    )
    actor2_id = cursor.lastrowid

    cursor.execute(
        """
        INSERT INTO Cast (first_name, last_name)
        VALUES (?, ?)
    """,
        ("Aaron", "Eckhart"),
    )
    actor3_id = cursor.lastrowid

    cursor.execute(
        """
        INSERT INTO Cast (first_name, last_name)
        VALUES (?, ?)
    """,
        ("Michael", "Caine"),
    )
    actor4_id = cursor.lastrowid

    cursor.execute(
        """
        INSERT INTO Movie_Cast (movie_id, actor_id)
        VALUES (?, ?)
    """,
        (movie_id, actor1_id),
    )

    cursor.execute(
        """
        INSERT INTO Movie_Cast (movie_id, actor_id)
        VALUES (?, ?)
    """,
        (movie_id, actor2_id),
    )

    cursor.execute(
        """
        INSERT INTO Movie_Cast (movie_id, actor_id)
        VALUES (?, ?)
    """,
        (movie_id, actor3_id),
    )

    cursor.execute(
        """
        INSERT INTO Movie_Cast (movie_id, actor_id)
        VALUES (?, ?)
    """,
        (movie_id, actor4_id),
    )

    cursor.execute(
        """
        INSERT INTO Genres (genre_name)
        VALUES (?)
    """,
        ("Action",),
    )
    genre1_id = cursor.lastrowid

    cursor.execute(
        """
        INSERT INTO Genres (genre_name)
        VALUES (?)
    """,
        ("Crime",),
    )
    genre2_id = cursor.lastrowid

    cursor.execute(
        """
            INSERT INTO Genres (genre_name)
            VALUES (?)
        """,
        ("Tragedy",),
    )
    genre3_id = cursor.lastrowid

    cursor.execute(
        """
            INSERT INTO Genres (genre_name)
            VALUES (?)
        """,
        ("Drama",),
    )
    genre4_id = cursor.lastrowid

    cursor.execute(
        """
            INSERT INTO Genres (genre_name)
            VALUES (?)
        """,
        ("Thriller",),
    )
    genre5_id = cursor.lastrowid

    cursor.execute(
        """
            INSERT INTO Genres (genre_name)
            VALUES (?)
        """,
        ("Superhero",),
    )
    genre6_id = cursor.lastrowid

    cursor.execute(
        """
        INSERT INTO Movie_Genres (movie_id, genre_id)
        VALUES(?, ?)
    """,
        (movie_id, genre1_id),
    )

    cursor.execute(
        """
        INSERT INTO Movie_Genres (movie_id, genre_id)
        VALUES(?, ?)
    """,
        (movie_id, genre2_id),
    )

    cursor.execute(
        """
            INSERT INTO Movie_Genres (movie_id, genre_id)
            VALUES(?, ?)
        """,
        (movie_id, genre3_id),
    )

    cursor.execute(
        """
            INSERT INTO Movie_Genres (movie_id, genre_id)
            VALUES(?, ?)
        """,
        (movie_id, genre4_id),
    )

    cursor.execute(
        """
            INSERT INTO Movie_Genres (movie_id, genre_id)
            VALUES(?, ?)
        """,
        (movie_id, genre5_id),
    )

    cursor.execute(
        """
            INSERT INTO Movie_Genres (movie_id, genre_id)
            VALUES(?, ?)
        """,
        (movie_id, genre6_id),
    )


if __name__ == "__main__":
    conn = sqlite3.connect("popcorn.db")
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    # create_tables(cursor)
    # insert_data(cursor)

    conn.commit()

    cursor.execute(
        """
        SELECT
            m.movie_name,
            m.release_year,
            m.age_rating,
            m.runtime,
            m.combined_rating,
            group_concat(DISTINCT d.first_name || " " || d.last_name) AS directors,
            group_concat(DISTINCT c.first_name || " " || c.last_name) AS cast,
            group_concat(DISTINCT w.first_name || " " || w.last_name) AS writers,
            group_concat(DISTINCT g.genre_name) AS genres

        FROM Movies m

        LEFT JOIN Movie_Directors md ON m.movie_id = md.movie_id
        LEFT JOIN Directors d ON md.director_id = d.director_id

        LEFT JOIN Movie_Cast mc on m.movie_id = mc.movie_id
        LEFT JOIN Cast c ON mc.actor_id = c.actor_id

        LEFT JOIN Movie_Writers mw ON m.movie_id = mw.movie_id
        LEFT JOIN Writers w ON mw.writer_id = w.writer_id

        LEFT JOIN Movie_Genres mg on m.movie_id = mg.movie_id
        LEFT JOIN Genres g ON mg.genre_id = g.genre_id

        GROUP BY m.movie_id
    """
    )

    movies = cursor.fetchall()
    for movie in movies:
        print(movie)

    conn.close()
