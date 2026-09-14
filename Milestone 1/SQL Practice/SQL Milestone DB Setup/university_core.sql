CREATE DATABASE IF NOT EXISTS university_core;

USE university_core;

DROP TABLE IF EXISTS Enrollments;

DROP TABLE IF EXISTS Courses;

DROP TABLE IF EXISTS Students;

DROP TABLE IF EXISTS Departments;

CREATE TABLE Departments (
    department_id INT PRIMARY KEY,
    department_name VARCHAR(50) NOT NULL
);

CREATE TABLE Students (
    student_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT,
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES Departments (department_id)
);

CREATE TABLE Courses (
    course_id VARCHAR(10) PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES Departments (department_id)
);

CREATE TABLE Enrollments (
    student_id INT,
    course_id VARCHAR(10),
    grade VARCHAR(5),
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES Students (student_id),
    FOREIGN KEY (course_id) REFERENCES Courses (course_id)
);

-- Insert Sample Data
INSERT INTO
    Departments
VALUES (1, 'Computer Science'),
    (2, 'Mathematics'),
    (3, 'Physics'),
    (4, 'Literature');

INSERT INTO
    Students
VALUES (101, 'Alice Smith', 20, 1),
    (102, 'Bob Johnson', 22, 2),
    (103, 'Clara Evans', 21, 3),
    (104, 'David Kumar', 23, 1);

INSERT INTO
    Courses
VALUES ('C101', 'Algorithms', 1),
    ('C102', 'Linear Algebra', 2),
    (
        'C103',
        'Quantum Mechanics',
        3
    ),
    (
        'C104',
        'Shakespearean Drama',
        4
    );

INSERT INTO
    Enrollments
VALUES (101, 'C101', 'A'),
    (101, 'C102', 'B+'),
    (101, 'C103', 'B+'),
    (101, 'C104', 'A-'),
    (102, 'C102', 'B'),
    (102, 'C103', 'A'),
    (103, 'C103', 'B-'),
    (103, 'C104', 'A'),
    (104, 'C101', 'A+'),
    (104, 'C102', 'C+'),
    (104, 'C103', 'B'),
    (104, 'C104', 'B');