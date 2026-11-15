-- ==============================================================================
-- Database: university_core
-- Solution File: university_core_solution.sql
-- Contains: Question 2 & Question 5
-- ==============================================================================

USE university_core;

-- ==============================================================================
-- Question 2: Student Enrollments with Grades and Department Names
--
-- Problem Statement:
--   Generate a report listing every student along with the courses they are
--   enrolled in, the grades they have received, and the departments offering
--   those courses.
--
-- Query Requirements:
--   Write a single SQL query to fetch the student-course enrollment details
--   joining Students, Courses, Enrollments, and Departments.
--
-- Required Output Columns:
--   student_id, student_name, course_id, course_name, grade, department_name
-- ==============================================================================

SELECT 
    s.student_id,
    s.name AS student_name,
    c.course_id,
    c.course_name,
    e.grade,
    d.department_name
FROM Enrollments e
JOIN Students s 
    ON e.student_id = s.student_id
JOIN Courses c 
    ON e.course_id = c.course_id
JOIN Departments d 
    ON c.department_id = d.department_id
ORDER BY 
    s.student_id, 
    c.course_id;


-- ==============================================================================
-- Question 5: Students Ranked by Course Enrollments
--
-- Problem Statement:
--   Rank students based on the number of courses they are enrolled in.
--
-- Query Requirements:
--   Assign a RANK and a DENSE_RANK to each student based on the number of courses
--   enrolled in descending order. Ties receive the same rank. Order the final
--   result by rank_by_enrollments.
--
-- Required Output Columns:
--   student_id, name, course_count, rank_by_enrollments, dense_rank_by_enrollments
-- ==============================================================================

SELECT 
    s.student_id,
    s.name,
    COUNT(e.course_id) AS course_count,
    RANK() OVER (
        ORDER BY COUNT(e.course_id) DESC
    ) AS rank_by_enrollments,
    DENSE_RANK() OVER (
        ORDER BY COUNT(e.course_id) DESC
    ) AS dense_rank_by_enrollments
FROM Students s
LEFT JOIN Enrollments e 
    ON s.student_id = e.student_id
GROUP BY 
    s.student_id, 
    s.name
ORDER BY 
    rank_by_enrollments, 
    s.student_id;
