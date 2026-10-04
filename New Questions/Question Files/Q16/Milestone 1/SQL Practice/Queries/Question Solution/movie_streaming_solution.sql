-- ==============================================================================
-- Database: movie_streaming
-- Solution File: movie_streaming_solution.sql
-- ==============================================================================

USE movie_streaming;

-- ------------------------------------------------------------------------------
-- Question 6: Movies Watched by Viewers of 'Life of Pi'
--
-- Problem Statement:
--   List all movies that have been watched by any user who has watched 'Life of Pi'.
--
-- Query Requirements:
--   Write a SQL query to retrieve movie_id and title. Duplicate movie titles
--   must not appear in the result. Only include movies watched by users who
--   have also watched 'Life of Pi'.
--
-- Required Output Columns:
--   movie_id, title
-- ------------------------------------------------------------------------------

SELECT DISTINCT
    m.movie_id,
    m.title
FROM Movies m
JOIN Watch_History wh 
    ON m.movie_id = wh.movie_id
WHERE wh.user_id IN (
    SELECT wh_sub.user_id
    FROM Watch_History wh_sub
    JOIN Movies m_sub 
        ON wh_sub.movie_id = m_sub.movie_id
    WHERE m_sub.title = 'Life of Pi'
)
ORDER BY 
    m.movie_id;

-- Optional Note: If you want to exclude 'Life of Pi' itself and show only OTHER
-- movies watched by those users, you can append:
-- AND m.title <> 'Life of Pi';
