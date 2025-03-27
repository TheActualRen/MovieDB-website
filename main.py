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
        genre_list=["Drama", "Prison Drama"],
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

    movies = myManager.cursor.fetchall()
    for movie in movies:
        print(movie)

    myManager.conn.close()
