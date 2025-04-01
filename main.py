from authManager import AuthManager
from dbManager import DBManager

if __name__ == "__main__":

    myManager = DBManager(
        movie_name="The Shawshank Redemption",
        release_year=1994,
        age_rating="15",
        runtime=144,
        combined_rating=9.3,
        director_list=[["Frank", "Darabont"]],
        writer_list=[["Stephen", "King"], ["Frank", "Darabont"]],
        actor_list=[["Tim", "Robbins"], ["Morgan", "Freeman"], ["Bob", "Gunton"]],
        genre_list=["Prison Drama", "Drama"],
    )

    myManager.create_tables()
    myManager.add_movie()

    myManager.cursor.execute(
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
