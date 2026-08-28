/*
===============================================================================
StudentDB - Simple Student Practice Database
Database engine: MySQL 8.0+

Purpose:
- Supports filtering students by marks
- Supports monthly enrollment aggregation and LAG practice
- Supports joining Students, Enrollments and Courses

This file contains only database creation and sample data.
It does not contain question solutions.
===============================================================================
*/

DROP DATABASE IF EXISTS StudentDB;
CREATE DATABASE StudentDB;
USE StudentDB;

/* ============================================================
   1. STUDENTS
   ============================================================ */
CREATE TABLE Students
(
    student_id INT PRIMARY KEY,
    student_name VARCHAR(100) NOT NULL,
    course VARCHAR(100) NOT NULL,
    marks INT NOT NULL,
    grade VARCHAR(5),

    CONSTRAINT chk_student_marks
        CHECK (marks BETWEEN 0 AND 100)
);

/* ============================================================
   2. COURSES
   ============================================================ */
CREATE TABLE Courses
(
    course_id INT PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL UNIQUE
);

/* ============================================================
   3. ENROLLMENTS
   ============================================================ */
CREATE TABLE Enrollments
(
    enrollment_id INT PRIMARY KEY,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    enrollment_date DATE NOT NULL,

    CONSTRAINT uq_student_course
        UNIQUE (student_id, course_id),

    CONSTRAINT fk_enrollment_student
        FOREIGN KEY (student_id)
        REFERENCES Students(student_id),

    CONSTRAINT fk_enrollment_course
        FOREIGN KEY (course_id)
        REFERENCES Courses(course_id)
);

/* ============================================================
   COURSES DATA
   ============================================================ */
INSERT INTO Courses
(course_id, course_name)
VALUES
(1, 'Database Management Systems'),
(2, 'SQL'),
(3, 'Python'),
(4, 'Computer Networks'),
(5, 'Data Engineering');

/* ============================================================
   STUDENTS DATA
   Includes the students needed for marks and enrollment practice.
   ============================================================ */
INSERT INTO Students
(student_id, student_name, course, marks, grade)
VALUES
(101, 'Ananya Rao',   'Database Management Systems', 88, 'A'),
(102, 'Rohan Mehta',  'SQL',                         74, 'B'),
(103, 'Meera Joshi',  'Python',                      82, 'A'),
(104, 'Rahul Verma',  'Database Management Systems', 76, 'B'),
(105, 'Kavya Singh',  'Data Engineering',            69, 'C'),
(106, 'Vikram Das',   'Computer Networks',            84, 'A'),
(107, 'Isha Kapoor',  'SQL',                         79, 'B'),
(108, 'Aman Gupta',   'Python',                      73, 'B'),
(109, 'Sneha Patel',  'Database Management Systems', 91, 'A'),
(110, 'Kabir Shah',   'Python',                      72, 'B'),
(111, 'Nisha Rao',    'Data Engineering',            87, 'A'),
(112, 'Dev Malhotra', 'Computer Networks',            65, 'C'),
(301, 'Aisha',         'SQL',                         78, 'B'),
(302, 'Rahul',         'SQL',                         92, 'A'),
(303, 'Neha',          'Python',                      85, 'A'),
(304, 'Arjun',         'SQL',                         67, 'C'),
(305, 'Priya',         'Python',                      95, 'A');

/* ============================================================
   ENROLLMENT DATA

   Monthly distribution for aggregation practice:
   January 2025  : 3 enrollments
   February 2025 : 5 enrollments
   March 2025    : 4 enrollments
   April 2025    : 6 enrollments

   July 2025 includes the three specific DBMS enrollments.
   ============================================================ */
INSERT INTO Enrollments
(enrollment_id, student_id, course_id, enrollment_date)
VALUES
/* January 2025 */
(1,  102, 2, '2025-01-05'),
(2,  103, 3, '2025-01-12'),
(3,  105, 5, '2025-01-20'),

/* February 2025 */
(4,  106, 4, '2025-02-03'),
(5,  107, 2, '2025-02-08'),
(6,  108, 3, '2025-02-14'),
(7,  111, 5, '2025-02-19'),
(8,  112, 4, '2025-02-25'),

/* March 2025 */
(9,  301, 2, '2025-03-04'),
(10, 303, 3, '2025-03-11'),
(11, 304, 2, '2025-03-18'),
(12, 305, 3, '2025-03-26'),

/* April 2025 */
(13, 102, 5, '2025-04-02'),
(14, 103, 1, '2025-04-07'),
(15, 105, 2, '2025-04-12'),
(16, 106, 3, '2025-04-17'),
(17, 107, 4, '2025-04-22'),
(18, 108, 5, '2025-04-28'),

/* July 2025: DBMS enrollment practice */
(19, 101, 1, '2025-07-10'),
(20, 104, 1, '2025-07-11'),
(21, 109, 1, '2025-07-13'),
(22, 110, 3, '2025-07-14');
