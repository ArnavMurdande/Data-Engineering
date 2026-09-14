-- ==============================================================================
-- Database: ATHLETICS_RESULTS_DB
-- Solution File: athletics_results_db_solution.sql
-- ==============================================================================

USE ATHLETICS_RESULTS_DB;

-- ------------------------------------------------------------------------------
-- Question 9: Event Average Finish Time
--
-- Problem Statement:
--   Generate a report that, for every recorded track performance, displays the
--   event name, athlete name, finish time in seconds, and the average finish
--   time of all recorded performances within the same event.
--
-- Query Requirements:
--   Use AVG() window function with PARTITION BY event_id. Include only
--   status = 'Recorded' (exclude Disqualified or DNS). Round average to
--   2 decimal places. Sort by event_name, finish_time, athlete_name.
--
-- Required Output Columns:
--   event_name, athlete_name, finish_time, avg_event_time
-- ------------------------------------------------------------------------------

SELECT 
    e.event_name,
    a.athlete_name,
    r.finish_time,
    ROUND(
        AVG(r.finish_time) OVER (PARTITION BY r.event_id), 
        2
    ) AS avg_event_time
FROM Results r
JOIN Events e 
    ON r.event_id = e.event_id
JOIN Athletes a 
    ON r.athlete_id = a.athlete_id
WHERE r.status = 'Recorded'
ORDER BY 
    e.event_name, 
    r.finish_time, 
    a.athlete_name;



--- ROUND () used to limit a numeric value with decimal values to a particular length.

--- Example : ROUND(123.456,2) -> 123.46

--- *** It Rounds off the Value to the nearest value. ***
