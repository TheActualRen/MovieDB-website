import sqlite3


class DBManager:
    def __init__(
        self,
        movie_name: str,
        release_year: int,
        age_rating: str,
        runtime: int,
        combined_rating: float,
        director_list: list[list[str]],
        writer_list: list[list[str]],
        actor_list: list[list[str]],
        genre_list: list[str],
    ):

        self.movie_name = movie_name
        self.release_year = release_year
        self.age_rating = age_rating
        self.runtime = runtime
        self.combined_rating = combined_rating

        # we can have these same elements more than once
        self.director_list = director_list
        self.writer_list = writer_list
        self.actor_list = actor_list
        self.genre_list = genre_list

        self.conn = sqlite3.connect("popcorn.db")
        self.cursor = self.conn.cursor()

        self.directors_ids = []
        self.writers_ids = []
        self.actors_ids= []
        self.genres_ids = []

    def create_users_table(self):
        self.cursor.execute(
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

    def create_movies_table(self):
        self.cursor.execute(
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

    def create_directors_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Directors (
                director_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                last_name TEXT
            );
        """
        )

    def create_movie_director_table(self):
        self.cursor.execute(
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

    def create_writers_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Writers (
                writer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                last_name TEXT
            );
        """
        )

    def create_movie_writers_table(self):
        self.cursor.execute(
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

    def create_cast_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Cast (
                actor_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                last_name TEXT
            );
        """
        )

    def create_movie_cast_table(self):
        self.cursor.execute(
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

    def create_genres_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Genres (
                genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
                genre_name TEXT UNIQUE
            );
        """
        )

    def create_movie_genres_table(self):
        self.cursor.execute(
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

    def create_comments_table(self):
        self.cursor.execute(
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

    def create_ratings_table(self):
        self.cursor.execute(
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

    def insert_movie_table(self):
        self.cursor.execute(
            """
            INSERT INTO Movies(movie_name, release_year, age_rating, runtime, combined_rating)
            VALUES (?, ?, ?, ?, ?)
        """,
            (
                self.movie_name,
                self.release_year,
                self.age_rating,
                self.runtime,
                self.combined_rating,
            ),
        )
        self.movie_id = self.cursor.lastrowid

    def insert_directors_table(self, director):
        try:
            self.cursor.execute(
                """
                INSERT INTO Directors (first_name, last_name) 
                VALUES (?, ?)
            """,
                (director[0], director[1]),
            )
            self.directors_ids.append(self.cursor.lastrowid)

        except sqlite3.IntegrityError:
            self.cursor.execute(
                """
                SELECT director_id FROM Directors WHERE first_name = ? AND last_name = ?
            """,
                (director[0], director[1]),
            )
            result = self.cursor.fetchone()

            if result:
                self.directors_ids.append(result[0])
            else:
                raise RuntimeError(
                    f"Failed to retrieve director_id for {director[0]} {director[1]}"
                )

    def link_movie_director(self, i):
        self.cursor.execute(
            """
                INSERT INTO Movie_Directors (movie_id, director_id)
                VALUES (?, ?)
            """,
            (self.movie_id, self.directors_ids[i]),
        )

    def insert_writers_table(self, writer):
        try:
            self.cursor.execute(
                """
                INSERT INTO Writers (first_name, last_name) 
                VALUES (?, ?)
            """,
                (writer[0], writer[1]),
            )
            self.writers_ids.append(self.cursor.lastrowid)

        except sqlite3.IntegrityError:
            self.cursor.execute(
                """
                SELECT writer_id FROM Writers WHERE first_name = ? AND last_name = ?
            """,
                (writer[0], writer[1]),
            )
            result = self.cursor.fetchone()

            if result:
                self.writers_ids.append(result[0])

            else:
                raise RuntimeError(
                    f"Failed to retrieve writer_id for {writer[0]} {writer[1]}"
                )

    def link_movie_writer(self, i):
        self.cursor.execute(
            """
                INSERT INTO Movie_Writers (movie_id, writer_id)
                VALUES (?, ?)
            """,
            (self.movie_id, self.writers_ids[i]),
        )

    def insert_cast_table(self, actor):
        try:
            self.cursor.execute(
                """
                INSERT INTO Cast (first_name, last_name)
                VALUES (?, ?)
            """,
                (actor[0], actor[1]),
            )
            self.actors_ids.append(self.cursor.lastrowid)

        except sqlite3.IntegrityError:
            self.cursor.execute(
                """
                SELECT actor_id FROM Cast WHERE first_name = ? AND last_name = ?
            """,
                (actor[0], actor[1]),
            )
            result = self.cursor.fetchone()

            if result:
                self.actors_ids.append(result[0])
            else:
                raise RuntimeError(
                    f"Failed to retrieve actor_id for {actor[0]} {actor[1]}"
                )

    def link_movie_cast(self, i):
        self.cursor.execute(
            """
                INSERT INTO Movie_Cast (movie_id, actor_id)
                VALUES (?, ?)
            """,
            (self.movie_id, self.actors_ids[i]),
        )

    def insert_genres_table(self, genre):
        try:
            self.cursor.execute(
                """
                INSERT INTO Genres (genre_name)
                VALUES (?)
            """,
                (genre,),
            )
            self.genres_ids.append(self.cursor.lastrowid)

        except sqlite3.IntegrityError:
            self.cursor.execute(
                """
                SELECT genre_id FROM Genres WHERE genre_name = ?
            """,
                (genre,),
            )
            result = self.cursor.fetchone()

            if result:
                self.genres_ids.append(result[0])
            else:
                raise RuntimeError(f"Failed to retrieve genre_id for {genre}")

    def link_movie_genre_table(self, i):
        self.cursor.execute(
            """
                INSERT INTO Movie_Genres (movie_id, genre_id)
                VALUES (?, ?) 
            """,
            (self.movie_id, self.genres_ids[i]),
        )

    def insert_comments_table(self):
        pass

    def insert_ratings_table(self):
        pass

    def create_tables(self):
        self.create_users_table()

        self.create_movies_table()

        self.create_directors_table()
        self.create_movie_director_table()

        self.create_writers_table()
        self.create_movie_writers_table()

        self.create_cast_table()
        self.create_movie_cast_table()

        self.create_genres_table()
        self.create_movie_genres_table()

        self.create_comments_table()

        self.create_ratings_table()

    def add_movie(self):
        self.insert_movie_table()

        for i in range(len(self.director_list)):
            self.insert_directors_table(self.director_list[i])
            self.link_movie_director(i)

        for i in range(len(self.writer_list)):
            self.insert_writers_table(self.writer_list[i])
            self.link_movie_writer(i)

        for i in range(len(self.actor_list)):
            self.insert_cast_table(self.actor_list[i])
            self.link_movie_cast(i)

        for i in range(len(self.genre_list)):
            self.insert_genres_table(self.genre_list[i])
            self.link_movie_genre_table(i)
