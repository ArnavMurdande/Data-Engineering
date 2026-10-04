CREATE DATABASE IF NOT EXISTS PATIENT_APPOINTMENTS_DB;

USE PATIENT_APPOINTMENTS_DB;

DROP TABLE IF EXISTS Appointments;

DROP TABLE IF EXISTS Patients;

CREATE TABLE Patients (
    patient_id INT PRIMARY KEY,
    patient_name VARCHAR(100) NOT NULL
);

CREATE TABLE Appointments (
    appointment_id INT PRIMARY KEY,
    patient_id INT,
    appointment_date DATE NOT NULL,
    fee DECIMAL(10, 2),
    FOREIGN KEY (patient_id) REFERENCES Patients (patient_id)
);

-- Insert Sample Data
INSERT INTO
    Patients
VALUES (1, 'Meera'),
    (2, 'Rohan'),
    (3, 'Sahil');

INSERT INTO
    Appointments
VALUES (801, 1, '2026-08-02', 700.00),
    (806, 1, '2026-08-08', 850.00),
    (814, 1, '2026-08-21', 700.00),
    (902, 2, '2026-08-04', 600.00),
    (909, 2, '2026-08-18', 750.00),
    (1001, 3, '2026-08-06', 900.00),
    (1008, 3, '2026-08-16', 900.00);