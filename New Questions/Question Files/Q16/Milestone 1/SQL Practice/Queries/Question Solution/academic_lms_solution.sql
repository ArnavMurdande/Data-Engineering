-- ==============================================================================
-- Database: academic_lms
-- Solution File: academic_lms_solution.sql
-- ==============================================================================

USE academic_lms;

-- ------------------------------------------------------------------------------
-- Question 3: Calculate the Average Assignment Score per Course
--
-- Problem Statement:
--   Calculate the average assignment score per course across submissions.
--
-- Query Requirements:
--   Join suitable tables (Courses, Assignments, and Submissions) to get
--   course name and average score.
--
-- Required Output Columns:
--   course_name, avg_score
-- ------------------------------------------------------------------------------

SELECT 
    c.course_name,
    AVG(s.score) AS avg_score
FROM Courses c
JOIN Assignments a 
    ON c.course_id = a.course_id
JOIN Submissions s 
    ON a.assignment_id = s.assignment_id
GROUP BY 
    c.course_id, 
    c.course_name
ORDER BY 
    avg_score DESC;
