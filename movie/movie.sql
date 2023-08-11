--  For Get Movies
select * from movie_movie where movie_status = 'showing';

-- For show comingsoon 
select * from movie_movie where movie_status = 'comingsoon';

-- See all movies
select * from movie_movie;


-- Get one movie
select * from movie_movie where id = 1;



-- Search Movie
select * from movie_movie WHERE name LIKE 'jaari%';


-- Filter movie
SELECT *
FROM movie_movie 
WHERE 
    (release_date BETWEEN 'start_date' AND 'end_date')
    OR (genre ILIKE '%genre1%' OR genre ILIKE '%genre2%')
    OR (language = 'nepali');


-- Movie LIke 
SELECT COUNT(*) AS like_count
FROM movie_like
WHERE movie_id = '1';


-- Like

insert into movie_like(id, movie, count)
values('1', 2, count+1);


-- Cinema hall and SHowtime View

SELECT
    ch.*,
    st.*,
    mv.*
FROM
    cinema_cinemahall AS ch
JOIN
    movie_showtime AS st ON ch.id = st.cinema_hall_id 
JOIN
    movie_movie as mv ON st.movie.id  = mv.id 
WHERE
    st.movie_id = 2
    AND st.show_date = '2023-08-30';








