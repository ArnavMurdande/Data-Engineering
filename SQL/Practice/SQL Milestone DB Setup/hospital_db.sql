CREATE DATABASE IF NOT EXISTS HOSPITAL_DB;

USE HOSPITAL_DB;

DROP TABLE IF EXISTS Bills;

DROP TABLE IF EXISTS Appointments;

DROP TABLE IF EXISTS Doctors;

DROP TABLE IF EXISTS Departments;

CREATE TABLE Departments (
    dept_id INT PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL
);

CREATE TABLE Doctors (
    doctor_id INT PRIMARY KEY,
    doctor_name VARCHAR(100) NOT NULL,
    dept_id INT,
    FOREIGN KEY (dept_id) REFERENCES Departments (dept_id)
);

CREATE TABLE Appointments (
    appointment_id INT PRIMARY KEY,
    doctor_id INT,
    appointment_date DATE NOT NULL,
    FOREIGN KEY (doctor_id) REFERENCES Doctors (doctor_id)
);

CREATE TABLE Bills (
    bill_id INT PRIMARY KEY,
    appointment_id INT,
    amount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (appointment_id) REFERENCES Appointments (appointment_id)
);

-- Insert Sample Data
INSERT INTO Departments VALUES (1, 'Cardiology'), (2, 'Neurology');

INSERT INTO
    Doctors
VALUES (1, 'Dr. Smith', 1),
    (2, 'Dr. Anand', 1),
    (3, 'Dr. Lee', 1),
    (4, 'Dr. Patel', 2),
    (5, 'Dr. Ray', 2);

INSERT INTO
    Appointments
VALUES (101, 1, '2025-11-17'),
    (102, 1, '2025-11-15'),
    (103, 2, '2025-11-16'),
    (104, 2, '2025-11-14'),
    (105, 3, '2025-11-14'),
    (106, 4, '2025-11-17'),
    (107, 4, '2025-11-16'),
    (108, 5, '2025-11-17');

INSERT INTO
    Bills
VALUES (201, 101, 800.00),
    (202, 102, 700.00),
    (203, 103, 600.00),
    (204, 104, 600.00),
    (205, 105, 1200.00),
    (206, 106, 1000.00),
    (207, 107, 1000.00),
    (208, 108, 900.00);