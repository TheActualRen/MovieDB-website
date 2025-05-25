import json

from authManager import AuthManager
from dbManager import DBManager

if __name__ == "__main__":

    with open("movies.json", "r") as f:
        movies = json.load(f)

    
    # Only tries to create the tables if a movie exists in the JSON
    if movies:
        setup_manager = DBManager(**movies[0])
        setup_manager.create_tables()
        setup_manager.conn.close()
        
    # Adds all movies from JSON to the db
    for movie in movies:
        manager = DBManager(**movie)
        manager.create_tables()
        manager.add_movie()
        manager.conn.close()  

    # Displays all entries at once after processing the movies
    # if movies:
    #     display_manager = DBManager(**movies[0])
    #     display_manager.display_entry()
    #     display_manager.conn.close()

    # Display all entries in a table
    if movies:
        db = DBManager(**movies[0])
        db.display_table()
        db.conn.close()


    myAuthManager = AuthManager(
        first_name="Bob",
        last_name="Smith",
        username="bsmith",
        password="password123",
        email="bsmith@gmail.com",
    )

    # print(myAuthManager.hashed_password)
