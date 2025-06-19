import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

const MovieDetail = () => {
  const { id } = useParams();
  const [movie, setMovie] = useState(null);

  useEffect(() => {
    fetch(`http://localhost:8000/movies/${id}/`)
      .then(res => {
        if (!res.ok) throw new Error("Movie not found");
        return res.json();
      })
      .then(data => setMovie(data))
      .catch(err => console.error("Fetch error:", err));
  }, [id]);

  if (!movie) return <p>Loading movie...</p>;

  return (
    <div>
      <h2>{movie.movie_name} ({movie.release_year})</h2>
      <p>Age Rating: {movie.age_rating}</p>
      <p>Runtime: {movie.runtime} minutes</p>
      <p>Rating: {movie.combined_rating}</p>
      <img src={`/${movie.poster}`} alt={movie.movie_name} width="200" />
    </div>
  );
};

export default MovieDetail;

