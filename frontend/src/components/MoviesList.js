import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

const MoviesList = () => {
  const [movies, setMovies] = useState([]);

  useEffect(() => {
    fetch('http://localhost:8000/movies/')
      .then(res => res.json())
      .then(data => setMovies(data))
      .catch(err => console.error("Fetch error:", err));
  }, []);

  return (
    <div>
      <h2>Movies</h2>
      <ul>
        {movies.map(movie => (
          <li key={movie.movie_id}>
            <Link to={`/movies/${movie.movie_id}`}>
              {movie.movie_name} ({movie.release_year})
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default MoviesList;

