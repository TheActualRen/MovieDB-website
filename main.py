from authManager import AuthManager
from dbManager import DBManager

if __name__ == "__main__":

    myManager = DBManager(
        movie_name="Spider-Man: Across the Spider-Verse",
        release_year=2023,
        age_rating="PG",
        runtime=140,
        combined_rating=8.5,
        director_list=[
            ["Joaquim", "Dos Santos"],
            ["Kemp", "Powers"],
            ["Justin K.", "Thompson"],
        ],
        writer_list=[
            ["Phill", "Lord"],
            ["Christopher", "Miller"],
            ["Dave", "Callaham"],
        ],
        actor_list=[
            ["Shameik", "Moore"],
            ["Hailee", "Steinfeld"],
            ["Brian Tyree", "Henry"],
        ],
        genre_list=[
            "Computer Animation",
            "Superhero",
            "Action",
            "Adventure",
            "Animation",
            "Family",
            "Fantasy",
        ],
    )

    # myManager.create_tables()
    # myManager.add_movie()

    myManager.cursor.execute(
        """
        SELECT
            m.movie_name,
            m.release_year,
            m.age_rating,
            m.runtime,
            m.combined_rating,

            GROUP_CONCAT(DISTINCT (d.first_name || " " || d.last_name), ", ") AS directors,
            GROUP_CONCAT(DISTINCT (c.first_name || " " || c.last_name), ", ") AS movie_cast,
            GROUP_CONCAT(DISTINCT (w.first_name || " " || w.last_name), ", ") AS writers,
            GROUP_CONCAT(DISTINCT g.genre_name, ", ") AS genres

        FROM Movies m

        LEFT JOIN Movie_Directors md ON m.movie_id = md.movie_id
        LEFT JOIN Directors d ON md.director_id = d.director_id
        LEFT JOIN Movie_Cast mc ON m.movie_id = mc.movie_id
        LEFT JOIN Cast c ON mc.actor_id = c.actor_id
        LEFT JOIN Movie_Writers mw ON m.movie_id = mw.movie_id
        LEFT JOIN Writers w ON mw.writer_id = w.writer_id
        LEFT JOIN Movie_Genres mg ON m.movie_id = mg.movie_id
        LEFT JOIN Genres g ON mg.genre_id = g.genre_id

        GROUP BY m.movie_id
        """
    )

    movies = myManager.cursor.fetchall()
    for movie in movies:
        print(movie)

    myManager.conn.close()

    myAuthManager = AuthManager(
        first_name="Bob",
        last_name="Smith",
        username="bsmith",
        password="password123",
        email="bsmith@gmail.com",
    )

    print(myAuthManager.hashed_password)
