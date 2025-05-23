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
        poster_path=None,
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
        self.poster_path = poster_path

        self.conn = sqlite3.connect("popcorn.db")
        self.cursor = self.conn.cursor()

        self.directors_ids: list[int] = []
        self.writers_ids: list[int] = []
        self.actors_ids: list[int] = []
        self.genres_ids: list[int] = []

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

        self.conn.commit()

    def create_movies_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Movies (
                movie_id INTEGER PRIMARY KEY AUTOINCREMENT,
                movie_name TEXT, 
                release_year INTEGER, 
                age_rating TEXT,
                runtime INTEGER,
                combined_rating REAL DEFAULT 0,
                poster TEXT,
                UNIQUE(movie_name, release_year, runtime)
            );
        """
        )
        self.conn.commit()

    def movie_exists(self):
        self.cursor.execute(
            """
            SELECT COUNT(*) FROM Movies
            WHERE movie_name = ?
            AND release_year = ?
            AND runtime = ?
        """,
            (self.movie_name, self.release_year, self.runtime),
        )
        self.conn.commit()
        return self.cursor.fetchone()[0] > 0

    def create_directors_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Directors (
                director_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                last_name TEXT,
                UNIQUE(first_name, last_name)
            );
        """
        )

        self.conn.commit()

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

        self.conn.commit()

    def create_writers_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Writers (
                writer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                last_name TEXT,
                UNIQUE(first_name, last_name)
            );
        """
        )

        self.conn.commit()

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

        self.conn.commit()

    def create_actors_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Actors (
                actor_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                last_name TEXT,
                UNIQUE(first_name, last_name)
            );
        """
        )

        self.conn.commit()

    def create_movie_actors_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Movie_Actors (
                movie_id INTEGER,
                actor_id INTEGER,
                PRIMARY KEY (movie_id, actor_id),
                FOREIGN KEY (movie_id) REFERENCES Movies(movie_id) ON DELETE CASCADE,
                FOREIGN KEY (actor_id) REFERENCES Actors(actor_id) ON DELETE CASCADE
            );
        """
        )

        self.conn.commit()

    def create_genres_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Genres (
                genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
                genre_name TEXT UNIQUE
            );
        """
        )

        self.conn.commit()

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

        self.conn.commit()

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

        self.conn.commit()

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

        self.conn.commit()

    def insert_movie_table(self):
        if self.movie_exists():
            print(f"Movie {self.movie_name} ({self.release_year}) already exists")

            self.cursor.execute(
                """
                SELECT movie_id FROM Movies WHERE movie_name = ? AND release_year = ? AND runtime = ?
            """,
                (self.movie_name, self.release_year, self.runtime),
            )
            self.movie_id = self.cursor.fetchone()[0]
            return

        self.cursor.execute(
            """
            INSERT OR IGNORE INTO Movies(movie_name, release_year, age_rating, runtime, combined_rating, poster)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (
                self.movie_name,
                self.release_year,
                self.age_rating,
                self.runtime,
                self.combined_rating,
                self.poster_path,
            ),
        )
        self.movie_id = self.cursor.lastrowid

        self.conn.commit()

    def insert_directors_table(self, director):
        self.cursor.execute(
            """
            INSERT OR IGNORE INTO Directors(first_name, last_name)
            VALUES (?, ?)
        """,
            (director[0], director[1]),
        )

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

        self.conn.commit()

    def link_movie_director(self, i):
        self.cursor.execute(
            """
                INSERT OR IGNORE INTO Movie_Directors (movie_id, director_id)
                VALUES (?, ?)
        """,
            (self.movie_id, self.directors_ids[i]),
        )

        self.conn.commit()

    def insert_writers_table(self, writer):
        self.cursor.execute(
            """
            INSERT OR IGNORE INTO Writers (first_name, last_name) 
            VALUES (?, ?)
        """,
            (writer[0], writer[1]),
        )

        self.conn.commit()

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

        self.conn.commit()

    def link_movie_writer(self, i):
        self.cursor.execute(
            """
                INSERT OR IGNORE INTO Movie_Writers (movie_id, writer_id)
                VALUES (?, ?)
            """,
            (self.movie_id, self.writers_ids[i]),
        )

        self.conn.commit()

    def insert_cast_table(self, actor):
        self.cursor.execute(
            """
            INSERT OR IGNORE INTO Actors (first_name, last_name)
            VALUES (?, ?)
        """,
            (actor[0], actor[1]),
        )

        self.cursor.execute(
            """
            SELECT actor_id FROM Actors WHERE first_name = ? AND last_name = ?
        """,
            (actor[0], actor[1]),
        )
        result = self.cursor.fetchone()

        if result:
            self.actors_ids.append(result[0])

        else:
            raise RuntimeError(f"Failed to retrieve actor_id for {actor[0]} {actor[1]}")

        self.conn.commit()

    def link_movie_actors(self, i):
        self.cursor.execute(
            """
                INSERT INTO Movie_Actors(movie_id, actor_id)
                VALUES (?, ?)
            """,
            (self.movie_id, self.actors_ids[i]),
        )

        self.conn.commit()

    def insert_genres_table(self, genre):
        self.cursor.execute(
            """
            INSERT OR IGNORE INTO Genres (genre_name)
            VALUES (?)
        """,
            (genre,),
        )

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

        self.conn.commit()

    def link_movie_genre_table(self, i):
        self.cursor.execute(
            """
                INSERT INTO Movie_Genres (movie_id, genre_id)
                VALUES (?, ?) 
            """,
            (self.movie_id, self.genres_ids[i]),
        )

        self.conn.commit()

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

        self.create_actors_table()
        self.create_movie_actors_table()

        self.create_genres_table()
        self.create_movie_genres_table()

        self.create_comments_table()

        self.create_ratings_table()

    def add_movie(self) -> bool:
        if self.movie_exists():
            print(f"Movie {self.movie_name} ({self.release_year}) already exists")
            return False

        self.insert_movie_table()

        for i in range(len(self.director_list)):
            self.insert_directors_table(self.director_list[i])
            self.link_movie_director(i)

        for i in range(len(self.writer_list)):
            self.insert_writers_table(self.writer_list[i])
            self.link_movie_writer(i)

        for i in range(len(self.actor_list)):
            self.insert_cast_table(self.actor_list[i])
            self.link_movie_actors(i)

        for i in range(len(self.genre_list)):
            self.insert_genres_table(self.genre_list[i])
            self.link_movie_genre_table(i)

        return True

    def display_entry(self):
        self.cursor.execute(
            """
            SELECT
                m.movie_name,
                m.release_year,
                m.age_rating,
                m.runtime,
                m.combined_rating,
                GROUP_CONCAT(DISTINCT d.first_name || ' ' || d.last_name) AS directors,
                GROUP_CONCAT(DISTINCT a.first_name || ' ' || a.last_name) AS actors,
                GROUP_CONCAT(DISTINCT w.first_name || ' ' || w.last_name) AS writers,
                GROUP_CONCAT(DISTINCT g.genre_name) AS genres
        FROM Movies m
        LEFT JOIN Movie_Directors md ON m.movie_id = md.movie_id
        LEFT JOIN Directors d ON md.director_id = d.director_id
        LEFT JOIN Movie_Actors ma ON m.movie_id = ma.movie_id
        LEFT JOIN Actors a ON ma.actor_id = a.actor_id
        LEFT JOIN Movie_Writers mw ON m.movie_id = mw.movie_id
        LEFT JOIN Writers w ON mw.writer_id = w.writer_id
        LEFT JOIN Movie_Genres mg ON m.movie_id = mg.movie_id
        LEFT JOIN Genres g ON mg.genre_id = g.genre_id
        GROUP BY m.movie_id
        
        """
        )

        rows = self.cursor.fetchall()

        if not rows:
            print("No Movies Found")
            return

        for row in rows:
            print(row)

    def wrap_text(self, text, width):
        if text == "N/A":
            return ["N/A"]

        lines = []
        current_line = []
        current_length = 0
        parts = text.split(", ")

        for part in parts:
            part_length = len(part)

            if current_line and (current_length + part_length + 2 > width):
                lines.append(", ".join(current_line))
                current_line = [part]
                current_length = part_length
            else:
                current_line.append(part)
                current_length += part_length + 2

        if current_line:
            lines.append(", ".join(current_line))

        truncated = []
        for line in lines:
            if len(line) > width:
                truncated.append(line[: width - 3] + "...")
            else:
                truncated.append(line)

        return truncated

    def display_table(self):
        self.cursor.execute(
            """
                SELECT
                    m.movie_name,
                    m.release_year,
                    m.age_rating,
                    m.runtime,
                    m.combined_rating,
                    GROUP_CONCAT(DISTINCT d.first_name || ' ' || d.last_name) AS directors,
                    GROUP_CONCAT(DISTINCT a.first_name || ' ' || a.last_name) AS actors,
                    GROUP_CONCAT(DISTINCT w.first_name || ' ' || w.last_name) AS writers,
                    GROUP_CONCAT(DISTINCT g.genre_name) AS genres
            FROM Movies m
            LEFT JOIN Movie_Directors md ON m.movie_id = md.movie_id
            LEFT JOIN Directors d ON md.director_id = d.director_id
            LEFT JOIN Movie_Actors ma ON m.movie_id = ma.movie_id
            LEFT JOIN Actors a ON ma.actor_id = a.actor_id
            LEFT JOIN Movie_Writers mw ON m.movie_id = mw.movie_id
            LEFT JOIN Writers w ON mw.writer_id = w.writer_id
            LEFT JOIN Movie_Genres mg ON m.movie_id = mg.movie_id
            LEFT JOIN Genres g ON mg.genre_id = g.genre_id
            GROUP BY m.movie_id
            
            """
        )

        rows = self.cursor.fetchall()

        if not rows:
            print("No Movies Found")
            return

        headers = [
            "Movie",
            "Release Year",
            "Age Rating",
            "Runtime (mins)",
            "Rating",
            "Directors",
            "Actors",
            "Writers",
            "Genres",
        ]

        wrap_columns = {5: 20, 6: 20, 7: 20, 8: 20}

        all_display_rows = []

        for row in rows:
            processed_row = []

            for item in row:
                if item is None or str(item).strip() == "":
                    processed_row.append("N/A")
                else:
                    processed_row.append(str(item))

            wrapped = {}
            max_lines = 0
            for col, width in wrap_columns.items():
                content = processed_row[col]
                wrapped_lines = self.wrap_text(content, width)
                wrapped[col] = wrapped_lines
                max_lines = max(max_lines, len(wrapped_lines))

            for line_num in range(max_lines):
                display_row = []
                for col_idx in range(len(processed_row)):
                    if col_idx in wrap_columns:
                        if line_num < len(wrapped[col_idx]):
                            display_row.append(wrapped[col_idx][line_num])
                        else:
                            display_row.append("")
                    else:
                        if line_num == 0:
                            display_row.append(processed_row[col_idx])
                        else:
                            display_row.append("")

                all_display_rows.append(display_row)

        column_widths = []

        for i in range(len(headers)):
            max_len = len(headers[i])

            for row in all_display_rows:
                if i < len(row):
                    max_len = max(max_len, len(row[i]))
            column_widths.append(max_len + 2) # + 2 for padding

        format_str = " | ".join([f"{{:<{width}}}" for width in column_widths])

        divider = "-" * (sum(column_widths) + 3 * (len(headers) - 1))
        print("\n" + divider)
        print(format_str.format(*headers))
        print(divider)


        for row in all_display_rows:
            print(format_str.format(*row))

        print(divider + "\n")

