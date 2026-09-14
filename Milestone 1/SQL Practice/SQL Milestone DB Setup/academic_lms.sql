CREATE DATABASE IF NOT EXISTS academic_lms;

USE academic_lms;

DROP TABLE IF EXISTS Submissions;

DROP TABLE IF EXISTS Assignments;

DROP TABLE IF EXISTS Enrollment;

DROP TABLE IF EXISTS Courses;

DROP TABLE IF EXISTS Instructor;

DROP TABLE IF EXISTS Students;

CREATE TABLE Students (
    student_id INT PRIMARY KEY,
    student_name VARCHAR(100),
    email VARCHAR(100),
    registration_date DATE
);

CREATE TABLE Instructor (
    instructor_id INT PRIMARY KEY,
    instructor_name VARCHAR(100),
    email VARCHAR(100),
    department VARCHAR(100)
);

CREATE TABLE Courses (
    course_id INT PRIMARY KEY,
    course_name VARCHAR(100),
    instructor_id INT,
    start_date DATE,
    end_date DATE,
    FOREIGN KEY (instructor_id) REFERENCES Instructor (instructor_id)
);

CREATE TABLE Enrollment (
    enrollment_id INT PRIMARY KEY,
    student_id INT,
    course_id INT,
    enrollment_date DATE,
    FOREIGN KEY (student_id) REFERENCES Students (student_id),
    FOREIGN KEY (course_id) REFERENCES Courses (course_id)
);

CREATE TABLE Assignments (
    assignment_id INT PRIMARY KEY,
    course_id INT,
    assignment_title VARCHAR(100),
    due_date DATE,
    max_score INT,
    FOREIGN KEY (course_id) REFERENCES Courses (course_id)
);

CREATE TABLE Submissions (
    submission_id INT PRIMARY KEY,
    student_id INT,
    assignment_id INT,
    submission_date DATETIME,
    score INT,
    FOREIGN KEY (student_id) REFERENCES Students (student_id),
    FOREIGN KEY (assignment_id) REFERENCES Assignments (assignment_id)
);

-- Insert Sample Data
INSERT INTO
    Students
VALUES (
        1,
        'Alice Johnson',
        'alice@example.com',
        '2024-01-05'
    ),
    (
        2,
        'Bob Smith',
        'bob@example.com',
        '2023-12-15'
    ),
    (
        3,
        'Charlie Brown',
        'charlie@example.com',
        '2023-11-20'
    ),
    (
        4,
        'David Williams',
        'david@example.com',
        '2023-10-10'
    ),
    (
        5,
        'Emma Davis',
        'emma@example.com',
        '2024-02-01'
    ),
    (
        6,
        'Frank Thomas',
        'frank@example.com',
        '2024-03-05'
    ),
    (
        7,
        'Grace Miller',
        'grace@example.com',
        '2024-02-18'
    );

INSERT INTO
    Instructor
VALUES (
        1,
        'Dr. John Doe',
        'john.doe@university.com',
        'Computer Science'
    ),
    (
        2,
        'Dr. Sarah Lee',
        'sarah.lee@university.com',
        'Mathematics'
    ),
    (
        3,
        'Dr. Michael Johnson',
        'michael.j@university.com',
        'Physics'
    );

INSERT INTO
    Courses
VALUES (
        1,
        'Database Management',
        1,
        '2024-01-10',
        '2024-06-30'
    ),
    (
        2,
        'Machine Learning',
        2,
        '2024-02-15',
        '2024-07-30'
    ),
    (
        3,
        'Data Structures',
        1,
        '2023-09-01',
        '2024-04-01'
    ),
    (
        4,
        'Quantum Mechanics',
        3,
        '2024-03-01',
        '2024-08-30'
    ),
    (
        5,
        'Calculus II',
        2,
        '2024-04-05',
        '2024-09-15'
    );

INSERT INTO
    Enrollment
VALUES (1, 1, 1, '2024-01-12'),
    (2, 2, 1, '2024-01-14'),
    (3, 3, 2, '2024-02-20'),
    (4, 4, 2, '2024-02-22'),
    (5, 5, 3, '2023-09-10'),
    (6, 6, 3, '2023-10-05'),
    (7, 7, 4, '2024-03-05'),
    (8, 1, 5, '2024-04-10'),
    (9, 2, 4, '2024-03-12'),
    (10, 3, 5, '2024-04-15');

INSERT INTO
    Assignments
VALUES (
        1,
        1,
        'SQL Basics Assignment',
        '2024-02-10',
        100
    ),
    (
        2,
        1,
        'Advanced SQL Queries',
        '2024-03-15',
        100
    ),
    (
        3,
        2,
        'Linear Regression Project',
        '2024-03-01',
        100
    ),
    (
        4,
        2,
        'Neural Networks Report',
        '2024-04-05',
        100
    ),
    (
        5,
        3,
        'Sorting Algorithms',
        '2023-10-10',
        100
    ),
    (
        6,
        3,
        'Graph Theory Assignment',
        '2023-12-15',
        100
    ),
    (
        7,
        4,
        'Schrodinger\'s Equation Analysis',
        '2024-04-01',
        100
    ),
    (
        8,
        5,
        'Integration Techniques',
        '2024-05-10',
        100
    );

INSERT INTO
    Submissions
VALUES (
        1,
        1,
        1,
        '2024-02-08 00:00:00',
        85
    ),
    (
        2,
        2,
        1,
        '2024-02-09 00:00:00',
        92
    ),
    (
        3,
        3,
        2,
        '2024-03-14 00:00:00',
        78
    ),
    (
        4,
        4,
        2,
        '2024-03-15 00:00:00',
        95
    ),
    (
        5,
        5,
        3,
        '2024-02-28 00:00:00',
        89
    ),
    (
        6,
        6,
        4,
        '2024-04-03 00:00:00',
        76
    ),
    (
        7,
        1,
        5,
        '2023-10-08 00:00:00',
        80
    ),
    (
        8,
        1,
        6,
        '2023-12-14 00:00:00',
        88
    ),
    (
        9,
        2,
        7,
        '2024-03-30 00:00:00',
        94
    ),
    (
        10,
        3,
        8,
        '2024-05-08 00:00:00',
        90
    );